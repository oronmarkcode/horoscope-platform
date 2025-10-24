"""Application configuration using Pydantic settings."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Horoscope Backend API"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Database
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/horoscope_db",
        description="Database connection URL"
    )
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT tokens"
    )
    access_token_expire_minutes: int = 30
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
