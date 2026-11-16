from __future__ import annotations

from pydantic import BaseModel


class OtpSendResponse(BaseModel):
    message: str
    email: str
