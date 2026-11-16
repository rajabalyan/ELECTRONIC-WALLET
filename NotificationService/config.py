from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class NotificationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="NOTIFICATION_", extra="ignore")
    app_name: str = "NotificationService"
    environment: str = Field(default="development", validation_alias=AliasChoices("NOTIFICATION_ENVIRONMENT", "ENVIRONMENT"))
    host: str = "0.0.0.0"
    port: int = 8004
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias=AliasChoices("NOTIFICATION_REDIS_URL", "REDIS_URL"))
    kafka_bootstrap_servers: str = Field(default="localhost:9092", validation_alias=AliasChoices("NOTIFICATION_KAFKA_BOOTSTRAP_SERVERS", "KAFKA_BOOTSTRAP_SERVERS"))
    smtp_host: str = Field(default="localhost", validation_alias=AliasChoices("NOTIFICATION_SMTP_HOST", "SMTP_HOST"))
    smtp_port: int = Field(default=1025, validation_alias=AliasChoices("NOTIFICATION_SMTP_PORT", "SMTP_PORT"))
    smtp_username: str = Field(default="", validation_alias=AliasChoices("NOTIFICATION_SMTP_USERNAME", "SMTP_USERNAME"))
    smtp_password: str = Field(default="", validation_alias=AliasChoices("NOTIFICATION_SMTP_PASSWORD", "SMTP_PASSWORD"))
    smtp_from: str = Field(default="no-reply@example.com", validation_alias=AliasChoices("NOTIFICATION_SMTP_FROM", "SMTP_FROM"))
    smtp_use_tls: bool = Field(default=False, validation_alias=AliasChoices("NOTIFICATION_SMTP_USE_TLS", "SMTP_USE_TLS"))
    email_mode: str = Field(default="development", validation_alias=AliasChoices("NOTIFICATION_EMAIL_MODE", "EMAIL_MODE"))
    otp_ttl_seconds: int = Field(default=300, validation_alias=AliasChoices("OTP_TTL_SECONDS", "NOTIFICATION_OTP_TTL_SECONDS"))
    otp_max_attempts: int = Field(default=5, validation_alias=AliasChoices("OTP_MAX_ATTEMPTS", "NOTIFICATION_OTP_MAX_ATTEMPTS"))
    log_level: str = "INFO"

settings = NotificationSettings()
