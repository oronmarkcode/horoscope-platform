from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import openai
from openai import AsyncOpenAI

from ...core.config import settings
from .ai_provider_base import (
    AIProvider,
    ChatInput,
    ChatMessage,
    ChatOutput,
    Credentials,
    EmbedInput,
    EmbedOutput,
    ProviderConfig,
    Role,
)


@dataclass
class OpenAIProviderConfig(ProviderConfig):
    model: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-ada-002"
    max_tokens: Optional[int] = None
    temperature: float = 0.7


@dataclass
class OpenAICredentials(Credentials):
    api_key: str
    base_url: Optional[str] = None

    @classmethod
    def from_settings(cls) -> "OpenAICredentials":
        """Create credentials from settings object."""
        return cls(
            api_key=settings.openai_api_key, base_url=settings.openai_base_url or None
        )


class OpenAIProvider(AIProvider):
    def __init__(
        self,
        credentials: Optional[OpenAICredentials] = None,
        config: Optional[OpenAIProviderConfig] = None,
    ):
        self.credentials = credentials or OpenAICredentials.from_settings()

        self.config = config or OpenAIProviderConfig(
            model=settings.openai_model,
            embedding_model=settings.openai_embedding_model,
            max_tokens=settings.openai_max_tokens,
            temperature=settings.openai_temperature,
        )

        self.client = AsyncOpenAI(
            api_key=self.credentials.api_key, base_url=self.credentials.base_url
        )

    async def generate(self, input: ChatInput) -> ChatOutput:
        try:
            messages = [
                {"role": msg["role"].value, "content": msg["content"]}
                for msg in input["messages"]
            ]

            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )

            return ChatOutput(
                text=response.choices[0].message.content,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                finish_reason=response.choices[0].finish_reason,
            )
        except Exception as e:
            raise Exception(f"OpenAI chat error: {str(e)}")

    async def embed(self, input: EmbedInput) -> EmbedOutput:
        try:
            response = await self.client.embeddings.create(
                model=self.config.embedding_model, input=input["texts"]
            )

            vectors = [embedding.embedding for embedding in response.data]
            dim = len(vectors[0]) if vectors else 0

            return EmbedOutput(vectors=vectors, dim=dim)
        except Exception as e:
            raise Exception(f"OpenAI embedding error: {str(e)}")
