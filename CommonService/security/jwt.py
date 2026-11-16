from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt


def create_access_token(subject: str, secret: str, expires_minutes: int = 60, extra_claims: dict[str, Any] | None = None, algorithm: str = "HS256") -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_access_token(token: str, secret: str, algorithm: str = "HS256") -> dict[str, Any]:
    return jwt.decode(token, secret, algorithms=[algorithm])
