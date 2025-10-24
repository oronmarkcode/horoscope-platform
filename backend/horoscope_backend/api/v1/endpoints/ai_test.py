"""AI testing endpoints."""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ....services.ai.ai_provider_base import ChatInput, ChatMessage, Role
from ....services.ai.factory import AIProviderFactory, ProviderType

router = APIRouter()


class TextInput(BaseModel):
    text: str
    provider: str = "openai"


class ChatResponse(BaseModel):
    response: str
    provider_info: Dict[str, Any]


@router.post("/test", response_model=ChatResponse)
async def test_ai_provider(input_data: TextInput):
    """Test AI provider with text input."""
    try:
        # Create provider
        provider = AIProviderFactory.create_provider(ProviderType(input_data.provider))

        # Create chat input
        chat_input = ChatInput(
            messages=[ChatMessage(role=Role.USER, content=input_data.text)]
        )

        # Generate response
        response = await provider.generate(chat_input)

        return ChatResponse(
            response=response["text"],
            provider_info={
                "provider": input_data.provider,
                "usage": response.get("usage"),
                "finish_reason": response.get("finish_reason"),
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI provider error: {str(e)}")


@router.get("/providers")
async def list_providers():
    """List available AI providers."""
    return {
        "providers": [provider.value for provider in ProviderType],
        "default": "openai",
    }
