from datetime import date
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....crud.horoscope_crud import get_user_config_by_user_id, update_user_config
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


@router.get("/profile", response_model=ProfileOut)
async def get_profile(
    auth: AuthResult = Depends(require_auth_separate_schemes),
    db: Session = Depends(get_db),
):
    cfg = get_user_config_by_user_id(db, auth.user_id)
    if not cfg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found"
        )
    return ProfileOut(
        name=cfg.name,
        dob=cfg.dob,
        timezone=cfg.timezone,
        daily_email_enabled=cfg.daily_email_enabled,
    )


@router.put("/profile", response_model=ProfileOut)
async def update_profile(
    payload: ProfileUpdate = Body(...),
    auth: AuthResult = Depends(require_auth_separate_schemes),
    db: Session = Depends(get_db),
):
    cfg = update_user_config(
        db,
        user_id=auth.user_id,
        name=payload.name,
        dob=payload.dob,
        timezone=payload.timezone,
        daily_email_enabled=payload.daily_email_enabled,
    )
    if not cfg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found"
        )
    return ProfileOut(
        name=cfg.name,
        dob=cfg.dob,
        timezone=cfg.timezone,
        daily_email_enabled=cfg.daily_email_enabled,
    )
