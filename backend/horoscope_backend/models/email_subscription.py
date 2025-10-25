from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, UniqueConstraint

from ..core.database import Base


class EmailSubscription(Base):
    __tablename__ = "email_subscription"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    is_enabled = Column(Boolean, nullable=False, default=False)
    verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
