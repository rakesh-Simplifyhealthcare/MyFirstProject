from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.key_vault import get_secret


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "FastAPI Starter Kit"
    environment: str = "local"
    debug: bool = False

    api_v1_prefix: str = "/api/v1"

    database_url: str = "sqlite+aiosqlite:///./app.db"

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    backend_cors_origins: list[str] = []


@lru_cache
def get_settings() -> Settings:
    settings = Settings()  # type: ignore[call-arg]
    settings.database_url = get_secret("database-url") or settings.database_url
    settings.secret_key = get_secret("secret-key") or settings.secret_key
    return settings
