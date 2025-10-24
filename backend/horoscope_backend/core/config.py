"""Application configuration using Pydantic settings."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Horoscope Backend API"
    app_version: str = "0.1.0"

    database_url: str | None = (
        "postgresql://postgres:postgres@localhost:5432/horoscope_db"
    )

    api_v1_prefix: str = "/api/v1"

    ai_provider: str | None = "openai"
    openai_api_key: str
    openai_model: str | None = "gpt-3.5-turbo"

    openai_base_url: str

    # JWT Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
