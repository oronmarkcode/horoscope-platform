"""Startup script for the application."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "horoscope_backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
