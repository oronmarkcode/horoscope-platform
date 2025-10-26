from datetime import date
from typing import Union

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....crud.horoscope_crud import get_user_config_by_user_id
from ....crud.usage_crud import get_usage_for_date
from ....models.usage import Usage
from ....services.auth.auth_deps import AuthResult, require_auth_separate_schemes
from ....utils.common import today_in_tz

router = APIRouter()


class UsageOut(BaseModel):
    kind: str
    user_id: int | None = None
    ip: str | None = None
    for_date: date | None = None
    attempts: int | None = 0
    credits_remaining: int | None = None


@router.get("/usage", response_model=UsageOut)
async def get_usage(
    request: Request,
    auth: AuthResult = Depends(require_auth_separate_schemes),
    db: Session = Depends(get_db),
):
    if auth.user_id:
        cfg = get_user_config_by_user_id(db, auth.user_id)
        tz = cfg.timezone if cfg else "UTC"
        user_id = auth.user_id
        ip = None
    else:
        tz = "UTC"
        user_id = None
        ip = request.client.host

    usage = get_usage_for_date(
        db, ip=ip or "", for_date=today_in_tz(tz), user_id=user_id
    )

    return UsageOut(
        kind=getattr(usage.kind, "value", str(usage.kind)),
        user_id=usage.user_id,
        ip=usage.ip,
        for_date=usage.for_date,
        attempts=usage.attempts,
        credits_remaining=usage.credits_remaining,
    )
