from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.horoscope_entry import HoroscopeEntry
from ..models.user_config import UserConfig


def get_user_config_by_user_id(db: Session, user_id: int) -> Optional[UserConfig]:
    return db.query(UserConfig).filter(UserConfig.user_id == user_id).first()


def create_horoscope_entry(
    db: Session,
    *,
    user_id: Optional[int],
    is_anonymous: bool,
    name: Optional[str],
    dob: Optional[date],
    zodiac_sign: str,
    for_date: date,
    variation: int,
    payload_json: dict,
) -> HoroscopeEntry:
    entry = HoroscopeEntry(
        user_id=user_id,
        is_anonymous=is_anonymous,
        name=name,
        dob=dob,
        zodiac_sign=zodiac_sign,
        for_date=for_date,
        variation=variation,
        payload_json=payload_json,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def list_horoscope_entries(
    db: Session,
    *,
    user_id: int,
    from_date: Optional[date],
    to_date: Optional[date],
    limit: int,
    offset: int,
) -> List[HoroscopeEntry]:
    q = db.query(HoroscopeEntry).filter(HoroscopeEntry.user_id == user_id)
    if from_date:
        q = q.filter(HoroscopeEntry.for_date >= from_date)
    if to_date:
        q = q.filter(HoroscopeEntry.for_date <= to_date)
    return q.order_by(HoroscopeEntry.for_date.desc()).offset(offset).limit(limit).all()


def get_horoscope_entry_by_id(db: Session, entry_id) -> Optional[HoroscopeEntry]:
    return db.query(HoroscopeEntry).filter(HoroscopeEntry.id == entry_id).first()
