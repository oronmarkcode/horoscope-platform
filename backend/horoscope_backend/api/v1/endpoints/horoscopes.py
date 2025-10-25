from dataclasses import asdict
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from zodiac_sign import get_zodiac_sign

from ....core.database import get_db
from ....crud.auth_crud import get_user_by_id
from ....crud.horoscope_crud import (
    create_horoscope_entry,
    get_horoscope_entry_by_id,
    get_user_config_by_user_id,
    list_horoscope_entries,
)
from ....services.ai.openai_client import OpenAIProvider, OpenAIProviderConfig
from ....services.auth.auth_deps import AuthResult, require_auth_separate_schemes
from ....services.horoscope_ai_service.horoscope_ai_service import HoroscopeAIService
from ....utils.common import today_in_tz

router = APIRouter()


class HoroscopeCreate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    timezone: Optional[str] = None
    for_date: Optional[date] = None
    variation: Optional[int] = 0


class HoroscopeEntryOut(BaseModel):
    id: str
    user_id: Optional[int] = None
    is_anonymous: bool
    name: Optional[str] = None
    dob: Optional[date] = None
    zodiac_sign: str
    for_date: date
    variation: int | None = 0


@router.post("/horoscopes", response_model=HoroscopeEntryOut)
async def create_horoscope(
    payload: HoroscopeCreate = Body(...),
    auth: AuthResult = Depends(require_auth_separate_schemes),
    db: Session = Depends(get_db),
):
    if not auth.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    cfg = get_user_config_by_user_id(db, auth.user_id)
    if not cfg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User configuration required",
        )
    name = payload.name or cfg.name
    dob = payload.dob or cfg.dob
    tz = payload.timezone or cfg.timezone

    is_anonymous = False
    user_id = auth.user_id

    for_d = payload.for_date or today_in_tz(tz)
    provider = OpenAIProvider()
    service = HoroscopeAIService(provider=provider, default_tz=tz)
    result = await service.generate_horoscope(
        name=name,
        dob=dob,
        tz=tz,
        on_date=for_d,
        variation=payload.variation or 0,
        strict=False,
    )
    sign = get_zodiac_sign(dob.month, dob.day)
    entry = create_horoscope_entry(
        db,
        user_id=user_id,
        is_anonymous=is_anonymous,
        name=name if is_anonymous else None,
        dob=dob if is_anonymous else None,
        zodiac_sign=sign,
        for_date=for_d,
        variation=payload.variation or 0,
        payload_json=asdict(result),
    )
    return HoroscopeEntryOut(
        id=str(entry.id),
        user_id=entry.user_id,
        is_anonymous=entry.is_anonymous,
        name=entry.name,
        dob=entry.dob,
        zodiac_sign=entry.zodiac_sign,
        for_date=entry.for_date,
        variation=entry.variation,
    )


@router.get("/horoscopes", response_model=List[HoroscopeEntryOut])
async def list_horoscopes(
    from_date: Optional[date] = Query(None, alias="from"),
    to_date: Optional[date] = Query(None, alias="to"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    auth: AuthResult = Depends(require_auth_separate_schemes),
    db: Session = Depends(get_db),
):
    if not auth.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only available for authenticated users",
        )
    rows = list_horoscope_entries(
        db,
        user_id=auth.user_id,
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        offset=offset,
    )
    return [
        HoroscopeEntryOut(
            id=str(r.id),
            user_id=r.user_id,
            is_anonymous=r.is_anonymous,
            name=r.name,
            dob=r.dob,
            zodiac_sign=r.zodiac_sign,
            for_date=r.for_date,
            variation=r.variation,
        )
        for r in rows
    ]


@router.get("/horoscopes/{id}", response_model=HoroscopeEntryOut)
async def get_horoscope(
    id: str = Path(...),
    auth: AuthResult = Depends(require_auth_separate_schemes),
    db: Session = Depends(get_db),
):
    row = get_horoscope_entry_by_id(db, id)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Horoscope entry not found"
        )
    if not auth.user_id or row.user_id != auth.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this entry is forbidden",
        )
    return HoroscopeEntryOut(
        id=str(row.id),
        user_id=row.user_id,
        is_anonymous=row.is_anonymous,
        name=row.name,
        dob=row.dob,
        zodiac_sign=row.zodiac_sign,
        for_date=row.for_date,
        variation=row.variation,
    )
