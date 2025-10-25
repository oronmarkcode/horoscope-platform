from fastapi import APIRouter, Depends

from ....services.auth.auth_deps import AuthResult, require_auth_separate_schemes

router = APIRouter()


@router.get("/")
async def health_check(auth: AuthResult = Depends(require_auth_separate_schemes)):
    return {"status": "healthy", "service": "horoscope-platform"}
