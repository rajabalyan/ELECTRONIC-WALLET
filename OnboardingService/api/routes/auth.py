from __future__ import annotations

import json
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status

from CommonService.cache import CacheStore, create_cache
from CommonService.security.jwt import create_access_token
from CommonService.security.password import verify_password
from OnboardingService.config import settings
from OnboardingService.repositories.user_repository import UserRepository
from OnboardingService.schemas.auth import LoginRequest, OtpValidationRequest, TokenResponse
from OnboardingService.services.notification_client import NotificationClient

router = APIRouter(tags=["auth"])


async def get_repository() -> UserRepository:
    return UserRepository()


async def get_cache() -> CacheStore:
    return create_cache(settings.redis_url)


@router.post("/user/login", response_model=TokenResponse)
async def login(payload: LoginRequest, repo: UserRepository = Depends(get_repository)) -> TokenResponse:
    user = await repo.get_by_mobile_or_username(payload.mobile_number)
    if user is None or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "invalid_credentials", "message": "Invalid username or password"})
    token = create_access_token(
        str(user["id"]),
        settings.jwt_secret,
        settings.jwt_expire_minutes,
        extra_claims={"mobile_number": user["mobile_number"]},
        algorithm=settings.jwt_algorithm,
    )
    return TokenResponse(access_token=token, token_type="bearer")


@router.post("/validate/otp")
async def validate_otp(payload: OtpValidationRequest, repo: UserRepository = Depends(get_repository), redis: CacheStore = Depends(get_cache)) -> dict:
    pending_raw = await redis.get(f"pending_signup:{payload.email}")
    if not pending_raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"code": "invalid_otp", "message": "Pending signup not found"})
    pending = json.loads(pending_raw)
    client = NotificationClient(settings.notification_service_url)
    validated = await client.validate_otp(payload.email, payload.otp)
    if not validated.get("valid"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"code": "invalid_otp", "message": "OTP validation failed"})
    user = await repo.create_user(
        name=pending["name"],
        email=pending["email"],
        mobile_number=pending["mobile_number"],
        date_of_birth=date.fromisoformat(pending["date_of_birth"]),
        password_hash=pending["password_hash"],
        identification_type=pending["identification_type"],
        identification_value=pending["identification_value"],
        status="ACTIVE",
    )
    await redis.delete(f"pending_signup:{payload.email}")
    return {"message": "User activated successfully", "user_id": user["id"]}
