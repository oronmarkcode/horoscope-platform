import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import UUID

from ..core.database import Base


class UsageKindEnum(str, PyEnum):
    REGEN_CREDITS = "regen_credits"
    ANON_ATTEMPTS = "anon_attempts"


class Usage(Base):
    __tablename__ = "usage_tracking"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kind = Column(SAEnum(UsageKindEnum, name="usage_kind_enum"), nullable=False)
    user_id = Column(Integer, nullable=True)
    ip = Column(String(64), nullable=True)
    for_date = Column(Date, nullable=True)
    attempts = Column(Integer, nullable=True, default=0)
    credits_remaining = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (
        CheckConstraint(
            "(user_id IS NOT NULL AND ip IS NULL) OR (user_id IS NULL AND ip IS NOT NULL)",
            name="ck_usage_tracking_exclusive_actor",
        ),
        UniqueConstraint(
            "ip",
            "kind",
            "for_date",
            name="uq_usage_tracking_anon_per_day",
            deferrable=False,
        ),
        UniqueConstraint(
            "user_id",
            "kind",
            name="uq_usage_tracking_user_kind",
            deferrable=False,
        ),
    )
