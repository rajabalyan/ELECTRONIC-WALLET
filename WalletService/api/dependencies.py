from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from CommonService.security.jwt import decode_access_token
from WalletService.config import settings

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "unauthorized", "message": "Missing or invalid bearer token"})
    try:
        payload = decode_access_token(credentials.credentials, settings.jwt_secret, settings.jwt_algorithm)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "unauthorized", "message": "Invalid or expired JWT"})
    return payload
