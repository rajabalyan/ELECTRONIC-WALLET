from __future__ import annotations

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from CommonService.config import normalize_database_url


class TransactionSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="TRANSACTION_", extra="ignore")
    app_name: str = "TransactionService"
    environment: str = Field(default="development", validation_alias=AliasChoices("TRANSACTION_ENVIRONMENT", "ENVIRONMENT"))
    host: str = "0.0.0.0"
    port: int = 8003
    db_url: str = Field(default="sqlite+aiosqlite:///./transaction.db", validation_alias=AliasChoices("TRANSACTION_DB_URL", "DB_URL"))
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias=AliasChoices("TRANSACTION_REDIS_URL", "REDIS_URL"))
    kafka_bootstrap_servers: str = Field(default="localhost:9092", validation_alias=AliasChoices("TRANSACTION_KAFKA_BOOTSTRAP_SERVERS", "KAFKA_BOOTSTRAP_SERVERS"))
    jwt_secret: str = Field(default="change-me-dev-secret", validation_alias=AliasChoices("TRANSACTION_JWT_SECRET", "JWT_SECRET"))
    jwt_algorithm: str = Field(default="HS256", validation_alias=AliasChoices("TRANSACTION_JWT_ALGORITHM", "JWT_ALGORITHM"))
    user_service_url: str = Field(default="http://localhost:8001", validation_alias=AliasChoices("ONBOARDING_SERVICE_URL", "TRANSACTION_USER_SERVICE_URL"))
    wallet_service_url: str = Field(default="http://localhost:8002", validation_alias=AliasChoices("WALLET_SERVICE_URL", "TRANSACTION_WALLET_SERVICE_URL"))
    txn_initiation_topic: str = Field(default="txn-initiation-topic", validation_alias=AliasChoices("TXN_INITIATION_TOPIC", "TRANSACTION_TXN_INITIATION_TOPIC"))
    txn_update_topic: str = Field(default="txn-update-topic", validation_alias=AliasChoices("TXN_UPDATE_KAFKA_TOPIC", "TRANSACTION_TXN_UPDATE_KAFKA_TOPIC"))
    log_level: str = "INFO"

    @model_validator(mode="after")
    def normalize_local_defaults(self) -> "TransactionSettings":
        self.db_url = normalize_database_url(self.db_url, "sqlite+aiosqlite:///./transaction.db", self.environment)
        return self

settings = TransactionSettings()
