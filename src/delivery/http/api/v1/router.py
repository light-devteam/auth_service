from fastapi import APIRouter

from src.contexts.jwk.delivery.http import jwk_router


router = APIRouter(prefix='/v1')
router.include_router(jwk_router)
