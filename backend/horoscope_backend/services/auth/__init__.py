"""Authentication package."""

from .auth_deps import (
    AuthResult,
    CurrentUser,
    auth_with_api_key_fallback,
    auth_with_separate_schemes,
    get_current_user,
    optional_auth,
    optional_auth_or_api_key,
    require_auth,
    require_auth_or_api_key,
    require_auth_separate_schemes,
    security,
    verify_api_key,
)
from .auth_service import (
    create_access_token,
    verify_token,
)

__all__ = [
    "create_access_token",
    "verify_token",
    "get_current_user",
    "require_auth",
    "optional_auth",
    "CurrentUser",
    "security",
    "verify_api_key",
    "AuthResult",
    "auth_with_api_key_fallback",
    "require_auth_or_api_key",
    "optional_auth_or_api_key",
    "auth_with_separate_schemes",
    "require_auth_separate_schemes",
]
