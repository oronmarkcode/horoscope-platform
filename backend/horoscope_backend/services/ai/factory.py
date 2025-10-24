from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional, Union

from .ai_provider_base import AIProvider, Credentials, ProviderConfig
from .openai_client import OpenAICredentials, OpenAIProvider, OpenAIProviderConfig


class ProviderType(str, Enum):
    OPENAI = "openai"


class AIProviderFactory:
    """Factory for creating AI provider instances."""

    @staticmethod
    def create_provider(
        provider_type: ProviderType,
        credentials: Optional[Credentials] = None,
        config: Optional[ProviderConfig] = None,
    ) -> AIProvider:
        if provider_type == ProviderType.OPENAI:
            creds = credentials or OpenAICredentials.from_settings()
            conf = config or OpenAIProviderConfig()
            return OpenAIProvider(credentials=creds, config=conf)

        raise ValueError(f"Unsupported provider type: {provider_type}")
