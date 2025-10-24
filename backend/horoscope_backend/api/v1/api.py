"""API v1 router."""

from fastapi import APIRouter

from .endpoints import health, horoscopes

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(horoscopes.router, prefix="/horoscopes", tags=["horoscopes"])
