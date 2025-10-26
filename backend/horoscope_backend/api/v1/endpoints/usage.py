from typing import Union

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....crud.usage_crud import get_attempts_for_date, get_user_credits
from ....services.auth.auth_deps import AuthResult, require_auth_separate_schemes
from ....utils.common import today_in_tz

router = APIRouter()


class UsageUserResponse(BaseModel):
    type: str
    credits_remaining: int


class UsageAnonResponse(BaseModel):
    type: str
    attempts_today: int


@router.get("/usage", response_model=Union[UsageUserResponse, UsageAnonResponse])
async def get_usage(
    request: Request,
    auth: AuthResult = Depends(require_auth_separate_schemes),
    db: Session = Depends(get_db),
):
    if auth.user_id:
        return UsageUserResponse(
            type="user",
            credits_remaining=get_user_credits(db, user_id=auth.user_id),
        )

    tz = request.headers.get("X-Timezone") or "UTC"
    attempts = get_attempts_for_date(
        db, ip=request.client.host, for_date=today_in_tz(tz)
    )
    return UsageAnonResponse(type="anon", attempts_today=attempts)
