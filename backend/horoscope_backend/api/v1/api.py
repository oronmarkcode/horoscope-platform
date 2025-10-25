"""API v1 router."""

from fastapi import APIRouter

from .endpoints import auth, health, horoscopes, profile, usage

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(profile.router, tags=["profile"])
api_router.include_router(horoscopes.router, tags=["horoscopes"])
api_router.include_router(usage.router, tags=["usage"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
