from __future__ import annotations

from CommonService.security.jwt import create_access_token
from OnboardingService.config import settings


class AuthService:
    def create_token(self, subject: str) -> str:
        return create_access_token(subject, settings.jwt_secret, settings.jwt_expire_minutes, algorithm=settings.jwt_algorithm)
