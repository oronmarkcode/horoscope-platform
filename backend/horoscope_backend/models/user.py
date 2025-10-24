"""User model."""

from sqlalchemy import Boolean, Column, String

from .base import BaseModel


class User(BaseModel):
    """User model."""

    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
