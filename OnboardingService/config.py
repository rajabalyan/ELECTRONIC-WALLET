from __future__ import annotations

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from CommonService.config import normalize_database_url


class OnboardingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="ONBOARDING_", extra="ignore")
    app_name: str = "OnboardingService"
    environment: str = Field(default="development", validation_alias=AliasChoices("ONBOARDING_ENVIRONMENT", "ENVIRONMENT"))
    host: str = "0.0.0.0"
    port: int = 8001
    db_url: str = Field(default="sqlite+aiosqlite:///./onboarding.db", validation_alias=AliasChoices("ONBOARDING_DB_URL", "DB_URL"))
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias=AliasChoices("ONBOARDING_REDIS_URL", "REDIS_URL"))
    kafka_bootstrap_servers: str = Field(default="localhost:9092", validation_alias=AliasChoices("ONBOARDING_KAFKA_BOOTSTRAP_SERVERS", "KAFKA_BOOTSTRAP_SERVERS"))
    jwt_secret: str = Field(default="change-me-dev-secret", validation_alias=AliasChoices("ONBOARDING_JWT_SECRET", "JWT_SECRET"))
    jwt_algorithm: str = Field(default="HS256", validation_alias=AliasChoices("ONBOARDING_JWT_ALGORITHM", "JWT_ALGORITHM"))
    jwt_expire_minutes: int = Field(default=60, validation_alias=AliasChoices("ONBOARDING_JWT_EXPIRE_MINUTES", "JWT_EXPIRE_MINUTES"))
    notification_service_url: str = Field(default="http://localhost:8004", validation_alias=AliasChoices("ONBOARDING_NOTIFICATION_SERVICE_URL", "NOTIFICATION_SERVICE_URL"))
    otp_ttl_seconds: int = Field(default=300, validation_alias=AliasChoices("OTP_TTL_SECONDS", "ONBOARDING_OTP_TTL_SECONDS"))
    otp_max_attempts: int = Field(default=5, validation_alias=AliasChoices("OTP_MAX_ATTEMPTS", "ONBOARDING_OTP_MAX_ATTEMPTS"))
    log_level: str = "INFO"

    @model_validator(mode="after")
    def normalize_local_defaults(self) -> "OnboardingSettings":
        self.db_url = normalize_database_url(self.db_url, "sqlite+aiosqlite:///./onboarding.db", self.environment)
        return self

settings = OnboardingSettings()
