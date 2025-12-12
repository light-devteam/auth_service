from fastapi import APIRouter

from src.contexts.jwk.delivery.http import jwks_router


router = APIRouter(
    prefix='/.well-known',
    tags=['Well Known'],
)
router.include_router(jwks_router)
