from __future__ import annotations

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from CommonService.config import normalize_database_url


class WalletSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="WALLET_", extra="ignore")
    app_name: str = "WalletService"
    environment: str = Field(default="development", validation_alias=AliasChoices("WALLET_ENVIRONMENT", "ENVIRONMENT"))
    host: str = "0.0.0.0"
    port: int = 8002
    db_url: str = Field(default="sqlite+aiosqlite:///./wallet.db", validation_alias=AliasChoices("WALLET_DB_URL", "DB_URL"))
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias=AliasChoices("WALLET_REDIS_URL", "REDIS_URL"))
    kafka_bootstrap_servers: str = Field(default="localhost:9092", validation_alias=AliasChoices("WALLET_KAFKA_BOOTSTRAP_SERVERS", "KAFKA_BOOTSTRAP_SERVERS"))
    initial_balance: str = Field(default="100.00", validation_alias=AliasChoices("WALLET_INITIAL_BALANCE", "INITIAL_BALANCE"))
    jwt_secret: str = Field(default="change-me-dev-secret", validation_alias=AliasChoices("WALLET_JWT_SECRET", "JWT_SECRET"))
    jwt_algorithm: str = Field(default="HS256", validation_alias=AliasChoices("WALLET_JWT_ALGORITHM", "JWT_ALGORITHM"))
    user_creation_topic: str = Field(default="user-creation-topic", validation_alias=AliasChoices("USER_CREATION_TOPIC", "WALLET_USER_CREATION_TOPIC"))
    txn_initiation_topic: str = Field(default="txn-initiation-topic", validation_alias=AliasChoices("TXN_INITIATION_TOPIC", "WALLET_TXN_INITIATION_TOPIC"))
    txn_update_topic: str = Field(default="txn-update-topic", validation_alias=AliasChoices("TXN_UPDATE_KAFKA_TOPIC", "WALLET_TXN_UPDATE_KAFKA_TOPIC"))
    log_level: str = "INFO"

    @model_validator(mode="after")
    def normalize_local_defaults(self) -> "WalletSettings":
        self.db_url = normalize_database_url(self.db_url, "sqlite+aiosqlite:///./wallet.db", self.environment)
        return self

settings = WalletSettings()
