"""API v1 router."""

from fastapi import APIRouter

from .endpoints import ai_test, auth, health, horoscopes

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(horoscopes.router, prefix="/horoscopes", tags=["horoscopes"])
api_router.include_router(ai_test.router, prefix="/ai", tags=["ai"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
