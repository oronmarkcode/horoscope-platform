"""Horoscope endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....models.horoscope import Horoscope

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_horoscopes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all horoscopes."""
    horoscopes = db.query(Horoscope).offset(skip).limit(limit).all()
    return [
        {
            "id": h.id,
            "sign": h.sign,
            "date": h.date.isoformat() if h.date else None,
            "content": h.content,
            "author": h.author,
            "created_at": h.created_at.isoformat() if h.created_at else None,
        }
        for h in horoscopes
    ]


@router.get("/{sign}", response_model=dict)
async def get_horoscope_by_sign(sign: str, db: Session = Depends(get_db)):
    """Get horoscope by sign."""
    horoscope = db.query(Horoscope).filter(Horoscope.sign == sign).first()
    if not horoscope:
        raise HTTPException(status_code=404, detail="Horoscope not found")

    return {
        "id": horoscope.id,
        "sign": horoscope.sign,
        "date": horoscope.date.isoformat() if horoscope.date else None,
        "content": horoscope.content,
        "author": horoscope.author,
        "created_at": horoscope.created_at.isoformat()
        if horoscope.created_at
        else None,
    }
