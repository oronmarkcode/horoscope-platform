from datetime import date

from sqlalchemy.orm import Session

from ..core.config import settings
from ..models.usage import Usage, UsageKindEnum


def track_user_attempt(
    db: Session, *, for_date: date, user_id: int | None = None, ip: str | None = None
) -> Usage:
    if user_id:
        usage_kind = UsageKindEnum.REGEN_CREDITS
        row = (
            db.query(Usage)
            .filter(
                Usage.user_id == user_id,
                Usage.kind == usage_kind,
                Usage.for_date == for_date,
            )
            .first()
        )
    else:
        usage_kind = UsageKindEnum.ANON_ATTEMPTS
        row = (
            db.query(Usage)
            .filter(
                Usage.ip == ip, Usage.kind == usage_kind, Usage.for_date == for_date
            )
            .first()
        )
    row = (
        db.query(Usage)
        .filter(Usage.user_id == user_id, Usage.kind == usage_kind)
        .first()
    )

    credits_remaining = (
        settings.registered_user_init_credits
        if user_id
        else settings.anon_user_init_credit
    )
    if not row:
        row = Usage(
            kind=usage_kind,
            user_id=user_id,
            attempts=1,
            for_date=for_date,
            ip=ip,
            credits_remaining=credits_remaining,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    row.attempts += 1
    db.commit()
    db.refresh(row)
    return row


def get_usage_for_date(
    db: Session, *, ip: str, for_date: date, user_id
) -> Usage | None:
    if user_id:
        return (
            db.query(Usage)
            .filter(
                Usage.user_id == user_id,
                Usage.for_date == for_date,
            )
            .first()
        )
    else:
        return (
            db.query(Usage)
            .filter(
                Usage.ip == ip,
                Usage.kind == UsageKindEnum.ANON_ATTEMPTS,
                Usage.for_date == for_date,
            )
            .first()
        )
