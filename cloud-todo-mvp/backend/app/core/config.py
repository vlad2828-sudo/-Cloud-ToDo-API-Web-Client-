from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="local", alias="APP_ENV")
    port: int = Field(default=8000, alias="PORT")
    database_url: str = Field(default="sqlite:///./todo_local.db", alias="DATABASE_URL")
    api_key: str = Field(default="dev-api-key-change-me", alias="API_KEY")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    cors_allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173", alias="CORS_ALLOWED_ORIGINS"
    )

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
