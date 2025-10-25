import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from ..core.database import Base


class UserConfig(Base):
    __tablename__ = "user_config"

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    name = Column(String(120), nullable=False)
    dob = Column(Date, nullable=False)
    timezone = Column(String(64), nullable=False, default="Europe/Amsterdam")
    daily_email_enabled = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
