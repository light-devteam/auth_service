from fastapi import APIRouter

from src.jwk.delivery.http.jwks import router as jwks_router


router = APIRouter(
    prefix='/.well-known',
    tags=['Well Known'],
)
router.include_router(jwks_router)
