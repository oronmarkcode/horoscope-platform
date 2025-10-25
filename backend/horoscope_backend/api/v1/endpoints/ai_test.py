from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, HTTPBearer
from pydantic import BaseModel

from ....models.user import User
from ....services.ai.ai_provider_base import ChatInput, ChatMessage, Role
from ....services.ai.factory import AIProviderFactory, ProviderType
from ....services.auth.auth_deps import (
    AuthResult,
    CurrentUser,
    get_current_user,
    require_auth_separate_schemes,
)

router = APIRouter()

# Security schemes for Swagger UI
bearer_scheme = HTTPBearer(auto_error=False, scheme_name="Bearer Token")
api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False, scheme_name="API Key")


class TextInput(BaseModel):
    text: str
    provider: str = "openai"


class ChatResponse(BaseModel):
    response: str
    provider_info: Dict[str, Any]
    user_id: Optional[int] = None


@router.post("/test", response_model=ChatResponse)
async def test_ai_provider(
    input_data: TextInput, current_user: CurrentUser = Depends(get_current_user)
):
    try:
        provider = AIProviderFactory.create_provider(ProviderType(input_data.provider))

        chat_input = ChatInput(
            messages=[ChatMessage(role=Role.USER, content=input_data.text)]
        )

        response = await provider.generate(chat_input)

        return ChatResponse(
            response=response["text"],
            provider_info={
                "provider": input_data.provider,
                "usage": response.get("usage"),
                "finish_reason": response.get("finish_reason"),
            },
            user_id=current_user.user_id,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI provider error: {str(e)}")


@router.post("/test-auth", response_model=ChatResponse)
async def test_ai_provider_auth_required(
    input_data: TextInput,
    auth: AuthResult = Depends(require_auth_separate_schemes),
    bearer_token: str = Security(bearer_scheme),
    api_key: str = Security(api_key_scheme),
):
    """Test AI provider with required authentication (JWT token or API key)."""
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
            user_id=auth.user_id,
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


@router.post("/debug-token")
async def debug_token(
    auth: AuthResult = Depends(require_auth_separate_schemes),
    bearer_token: str = Security(bearer_scheme),
    api_key: str = Security(api_key_scheme),
):
    """Debug endpoint to check authentication status."""
    return {
        "is_authenticated": auth.is_authenticated,
        "auth_type": auth.auth_type,
        "user_id": auth.user_id,
        "has_user": auth.user is not None,
        "has_api_key": auth.api_key is not None,
    }
