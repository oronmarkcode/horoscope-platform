"""API v1 router."""

from fastapi import APIRouter

from .endpoints import ai_horoscopes, health, horoscopes

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(horoscopes.router, prefix="/horoscopes", tags=["horoscopes"])
api_router.include_router(ai_horoscopes.router, prefix="/ai", tags=["ai"])
