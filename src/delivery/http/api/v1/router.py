from fastapi import APIRouter

from src.contexts.jwk.delivery.http import jwk_router
from src.contexts.authentication.delivery.http import accounts_router, providers_router


router = APIRouter(prefix='/v1')
router.include_router(jwk_router)
router.include_router(accounts_router)
router.include_router(providers_router)
