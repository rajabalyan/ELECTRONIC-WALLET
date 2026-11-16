from __future__ import annotations

from OnboardingService.config import OnboardingSettings
from CommonService.security.jwt import create_access_token, decode_access_token
from CommonService.security.password import hash_password, verify_password


def test_password_hashing_roundtrip() -> None:
    raw = "super-secret"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True


def test_jwt_roundtrip() -> None:
    token = create_access_token("user-42", "secret123", 60, algorithm="HS256")
    payload = decode_access_token(token, "secret123", algorithm="HS256")
    assert payload["sub"] == "user-42"


def test_onboarding_local_db_falls_back_to_sqlite(monkeypatch) -> None:
    monkeypatch.setenv("ONBOARDING_DB_URL", "mysql+aiomysql://root:root@localhost:3306/ewallet_onboarding")
    settings = OnboardingSettings()
    assert settings.db_url == "sqlite+aiosqlite:///./onboarding.db"


def test_onboarding_respects_production_environment(monkeypatch) -> None:
    database_url = "mysql+aiomysql://wallet_user:strong-password@db.example:3306/ewallet"
    monkeypatch.setenv("ONBOARDING_ENVIRONMENT", "production")
    monkeypatch.setenv("ONBOARDING_DB_URL", database_url)

    settings = OnboardingSettings()

    assert settings.environment == "production"
    assert settings.db_url == database_url
