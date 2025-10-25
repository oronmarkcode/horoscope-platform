from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ...core.config import settings
from ...core.database import get_db
from ...crud.auth_crud import get_user_by_id
from ...models.user import User
from .auth_service import verify_token

security = HTTPBearer(auto_error=False)


class CurrentUser:
    def __init__(self, user: Optional[User] = None):
        self.user = user
        self.is_authenticated = user is not None
        self.user_id = user.id if user else None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> CurrentUser:
    if not credentials:
        return CurrentUser()

    payload = verify_token(credentials.credentials)
    if not payload:
        return CurrentUser()

    user_id = payload.get("sub")
    if not user_id:
        return CurrentUser()

    user = get_user_by_id(db, int(user_id))
    if not user or not user.is_active:
        return CurrentUser()

    return CurrentUser(user=user)


async def require_auth(current_user: CurrentUser = Depends(get_current_user)) -> User:
    if not current_user.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user.user


async def get_user_if_bearer(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if not credentials:
        return None

    payload = verify_token(credentials.credentials)
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    user = get_user_by_id(db, int(user_id))
    if not user or not user.is_active:
        return None

    return user


def verify_api_key(api_key: str) -> bool:
    return api_key == settings.api_key


class AuthResult:
    def __init__(self, user: Optional[User] = None, api_key: Optional[str] = None):
        self.user = user
        self.api_key = api_key
        self.is_authenticated = user is not None or api_key is not None
        self.user_id = user.id if user else None
        self.auth_type = "user" if user else "api_key" if api_key else "none"


async def auth_with_separate_schemes(
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> AuthResult:
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]

        payload = verify_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                user = get_user_by_id(db, int(user_id))
                if user and user.is_active:
                    return AuthResult(user=user)

        if verify_api_key(token):
            return AuthResult(api_key=token)

    if x_api_key and verify_api_key(x_api_key):
        return AuthResult(api_key=x_api_key)

    return AuthResult()


async def require_auth_separate_schemes(
    auth_result: AuthResult = Depends(auth_with_separate_schemes),
) -> AuthResult:
    if not auth_result.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required (Bearer token or X-API-Key)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_result
