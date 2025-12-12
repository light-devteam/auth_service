from fastapi import APIRouter

from src.jwk.delivery.http.jwk import router as jwk_router


router = APIRouter(prefix='/v1')
router.include_router(jwk_router)
