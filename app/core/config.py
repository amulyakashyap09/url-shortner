from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "My Application"
    debug: bool = False
    database_url: str = "sqlite:///./test.db"
    base_url: str = "your-base-url"
    secret_key: str = "your-secret-key"
    algorithm: str = "your-algorithm"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
