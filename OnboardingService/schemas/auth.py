from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mobile_number: str = Field(..., min_length=8, max_length=25)
    password: str = Field(..., min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OtpValidationRequest(BaseModel):
    email: str
    otp: str = Field(..., min_length=6, max_length=6)
