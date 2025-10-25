import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..core.database import Base


class HoroscopeEntry(Base):
    __tablename__ = "horoscope_entry"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    is_anonymous = Column(Boolean, nullable=False, default=False)
    name = Column(String(120), nullable=True)
    dob = Column(Date, nullable=True)
    zodiac_sign = Column(String(32), nullable=False)
    for_date = Column(Date, nullable=False)
    variation = Column(Integer, nullable=False, default=0)
    payload_json = Column(JSONB, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
