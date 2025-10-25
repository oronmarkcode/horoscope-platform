from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query
from pydantic import BaseModel

from ....services.auth.auth_deps import AuthResult, require_auth_separate_schemes

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
    variation: int


@router.post("/horoscopes", response_model=HoroscopeEntryOut)
async def create_horoscope(
    payload: HoroscopeCreate = Body(...),
    auth: AuthResult = Depends(require_auth_separate_schemes),
):
    raise NotImplementedError


@router.get("/horoscopes", response_model=List[HoroscopeEntryOut])
async def list_horoscopes(
    from_date: Optional[date] = Query(None, alias="from"),
    to_date: Optional[date] = Query(None, alias="to"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    auth: AuthResult = Depends(require_auth_separate_schemes),
):
    raise NotImplementedError


@router.get("/horoscopes/{id}", response_model=HoroscopeEntryOut)
async def get_horoscope(
    id: str = Path(...),
    auth: AuthResult = Depends(require_auth_separate_schemes),
):
    raise NotImplementedError
