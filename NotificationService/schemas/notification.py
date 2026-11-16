from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OtpRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str


class OtpValidationRequest(BaseModel):
    email: str
    otp: str = Field(..., min_length=6, max_length=6)
