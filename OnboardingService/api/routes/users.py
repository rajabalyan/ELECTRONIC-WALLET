from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from CommonService.cache import CacheStore, create_cache
from OnboardingService.api.dependencies import get_current_user
from OnboardingService.config import settings
from OnboardingService.repositories.user_repository import UserRepository
from OnboardingService.schemas.user import CreateUserRequest, UserResponse
from OnboardingService.services.notification_client import NotificationClient
from CommonService.security.password import hash_password

router = APIRouter(tags=["users"])


async def get_repository() -> UserRepository:
    return UserRepository()


async def get_cache() -> CacheStore:
    return create_cache(settings.redis_url)


@router.post("/create/user", status_code=status.HTTP_201_CREATED)
async def create_user(payload: CreateUserRequest, repo: UserRepository = Depends(get_repository), redis: CacheStore = Depends(get_cache)) -> dict:
    existing = await repo.get_by_email_or_mobile_or_id(payload.email, payload.mobile_number, payload.identification_value)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"code": "duplicate_resource", "message": "User with same email, mobile, or identification already exists"})
    signup = {
        "name": payload.name,
        "email": payload.email,
        "mobile_number": payload.mobile_number,
        "date_of_birth": payload.date_of_birth.isoformat(),
        "password_hash": hash_password(payload.password),
        "identification_type": payload.identification_type,
        "identification_value": payload.identification_value,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await redis.setex(f"pending_signup:{payload.email}", settings.otp_ttl_seconds, json.dumps(signup))
    client = NotificationClient(settings.notification_service_url)
    notification_result = await client.send_otp(payload.email)
    response = {"message": "User registration initiated. Please verify your OTP.", "email": payload.email}
    development_otp = notification_result.get("development_otp")
    if settings.environment.lower() in {"development", "local", "test"} and development_otp:
        response["development_otp"] = development_otp
    return response


@router.get("/validate/user/{username}")
async def validate_user(username: str, repo: UserRepository = Depends(get_repository)) -> dict:
    exists = await repo.user_exists(username)
    return {"exists": exists}


@router.get("/me", response_model=UserResponse)
async def get_my_profile(user: dict = Depends(get_current_user), repo: UserRepository = Depends(get_repository)) -> UserResponse:
    user_id = user.get("sub")
    record = await repo.get_by_id(user_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "user_not_found", "message": "User not found"})
    return UserResponse.model_validate(record)
