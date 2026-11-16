from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    mobile_number: str = Field(..., min_length=10, max_length=20)
    date_of_birth: date
    password: str = Field(..., min_length=8, max_length=128)
    identification_type: str = Field(..., min_length=2, max_length=40)
    identification_value: str = Field(..., min_length=3, max_length=150)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    mobile_number: str
    identification_type: str
    identification_value: str
    status: str
