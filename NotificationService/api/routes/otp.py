from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from CommonService.cache import create_cache
from NotificationService.config import settings
from NotificationService.schemas.notification import OtpValidationRequest
from NotificationService.services.email_service import EmailService
from NotificationService.services.otp_service import OtpService

router = APIRouter(tags=["notifications"])


@router.post("/otp/send/otp/{email}")
async def send_otp(email: str) -> dict:
    otp = OtpService.generate_otp()
    redis = create_cache(settings.redis_url)
    await redis.setex(f"otp:{email}", settings.otp_ttl_seconds, otp)
    await redis.setex(f"otp_attempts:{email}", settings.otp_ttl_seconds, 0)
    email_service = EmailService()
    await email_service.send_otp(email, otp)
    response = {"message": "OTP sent", "email": email}
    if settings.email_mode.lower() == "development" and settings.environment.lower() in {"development", "local", "test"}:
        response["development_otp"] = otp
    return response


@router.post("/otp/validate")
async def validate_otp(payload: OtpValidationRequest) -> dict:
    redis = create_cache(settings.redis_url)
    stored = await redis.get(f"otp:{payload.email}")
    attempts_raw = await redis.get(f"otp_attempts:{payload.email}") or "0"
    attempts = int(attempts_raw)
    if stored is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"code": "invalid_otp", "message": "OTP expired or missing"})
    if attempts >= settings.otp_max_attempts:
        await redis.delete(f"otp:{payload.email}")
        await redis.delete(f"otp_attempts:{payload.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"code": "invalid_otp", "message": "OTP attempt limit reached"})
    if stored != payload.otp:
        await redis.setex(f"otp_attempts:{payload.email}", settings.otp_ttl_seconds, attempts + 1)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"code": "invalid_otp", "message": "OTP validation failed"})
    await redis.delete(f"otp:{payload.email}")
    await redis.delete(f"otp_attempts:{payload.email}")
    return {"valid": True, "message": "OTP validated"}
