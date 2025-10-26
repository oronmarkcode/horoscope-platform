from datetime import date

from sqlalchemy.orm import Session

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
    if not row:
        row = Usage(
            kind=usage_kind,
            user_id=user_id,
            attempts=1,
            for_date=for_date,
            ip=ip,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    row.attempts += 1
    db.commit()
    db.refresh(row)
    return row
