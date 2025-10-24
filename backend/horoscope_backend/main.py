"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from .api.v1.api import api_router
from .core.config import settings

# Import models to ensure they are registered with Base
from .models import base, horoscope, user  # noqa

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check endpoints",
        },
        {
            "name": "horoscopes",
            "description": "Horoscope management endpoints",
        },
        {
            "name": "ai",
            "description": "AI provider testing endpoints",
        },
        {
            "name": "authentication",
            "description": "User authentication endpoints",
        },
    ],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description="API that supports both JWT token and API key authentication",
        routes=app.routes,
    )

    # Add separate security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token",
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "Enter your API key",
        },
    }

    # Remove global security requirement - let endpoints define their own
    if "security" in openapi_schema:
        del openapi_schema["security"]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Horoscope Backend API", "version": settings.app_version}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
