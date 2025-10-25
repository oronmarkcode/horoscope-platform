from typing import Union

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ....services.auth.auth_deps import AuthResult, require_auth_separate_schemes

router = APIRouter()


class UsageUserResponse(BaseModel):
    type: str
    credits_remaining: int


class UsageAnonResponse(BaseModel):
    type: str
    attempts_today: int


@router.get("/usage", response_model=Union[UsageUserResponse, UsageAnonResponse])
async def get_usage(auth: AuthResult = Depends(require_auth_separate_schemes)):
    raise NotImplementedError
