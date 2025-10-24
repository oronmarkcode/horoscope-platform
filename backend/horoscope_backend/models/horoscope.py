"""Horoscope model."""

from sqlalchemy import Column, String, Text, Date
from .base import BaseModel


class Horoscope(BaseModel):
    """Horoscope model."""
    
    sign = Column(String(50), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=True)
