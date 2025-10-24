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
        description="Database connection URL",
    )

    # API
    api_v1_prefix: str = "/api/v1"

    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT tokens",
    )
    access_token_expire_minutes: int = 30

    # AI Provider Configuration
    ai_provider: str = Field(
        default="openai",
        description="AI provider to use (openai, anthropic, google, azure)",
    )
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_model: str = Field(
        default="gpt-3.5-turbo", description="OpenAI model to use"
    )
    openai_organization: str = Field(
        default="", description="OpenAI organization ID (optional)"
    )
    openai_base_url: str = Field(
        default="", description="Custom OpenAI base URL (optional)"
    )
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    google_api_key: str = Field(default="", description="Google AI API key")
    azure_api_key: str = Field(default="", description="Azure OpenAI API key")
    azure_endpoint: str = Field(default="", description="Azure OpenAI endpoint")
    azure_api_version: str = Field(
        default="2023-12-01-preview", description="Azure OpenAI API version"
    )

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
