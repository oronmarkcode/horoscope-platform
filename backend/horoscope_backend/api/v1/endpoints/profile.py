from datetime import date
from typing import Optional

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel

from ....services.auth.auth_deps import AuthResult, require_auth_separate_schemes

router = APIRouter()


class ProfileOut(BaseModel):
    name: str
    dob: date
    timezone: str
    daily_email_enabled: bool


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    timezone: Optional[str] = None
    daily_email_enabled: Optional[bool] = None


class EmailSubscriptionOut(BaseModel):
    user_id: int
    is_enabled: bool
    verified: bool


class EmailSubscriptionUpdate(BaseModel):
    is_enabled: bool


@router.get("/profile", response_model=ProfileOut)
async def get_profile(auth: AuthResult = Depends(require_auth_separate_schemes)):
    raise NotImplementedError


@router.put("/profile", response_model=ProfileOut)
async def update_profile(
    payload: ProfileUpdate = Body(...),
    auth: AuthResult = Depends(require_auth_separate_schemes),
):
    raise NotImplementedError


@router.get("/email-subscription", response_model=EmailSubscriptionOut)
async def get_email_subscription(
    auth: AuthResult = Depends(require_auth_separate_schemes),
):
    raise NotImplementedError


@router.put("/email-subscription", response_model=EmailSubscriptionOut)
async def update_email_subscription(
    payload: EmailSubscriptionUpdate = Body(...),
    auth: AuthResult = Depends(require_auth_separate_schemes),
):
    raise NotImplementedError
