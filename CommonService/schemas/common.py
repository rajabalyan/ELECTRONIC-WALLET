from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str


class ErrorResponse(BaseModel):
    code: str
    message: str


class MessageResponse(BaseModel):
    message: str
    data: dict | None = None
