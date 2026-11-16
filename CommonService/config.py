from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


def normalize_database_url(url: str | None, default_url: str, environment: str | None = None) -> str:
    if not url:
        return default_url

    normalized_environment = (environment or "").strip().lower()
    is_local_environment = normalized_environment in {"development", "local", "test"}
    mysql_local_pattern = (
        url.startswith("mysql+")
        or url.startswith("mysql://")
        or url.startswith("mysql+pymysql://")
        or url.startswith("mysql+aiomysql://")
    ) and "localhost" in url and "root" in url

    if is_local_environment and mysql_local_pattern:
        return default_url
    return url


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    environment: str = "development"
    log_level: str = "INFO"
