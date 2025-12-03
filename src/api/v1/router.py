from fastapi import APIRouter

from src.api.v1.healthcheck import router as health_router
from src.api.v1.jwk import router as jwk_router
from src.api.v1.session import router as session_router
from src.api.v1.app import router as app_router

router = APIRouter(prefix='/v1')
router.include_router(health_router)
router.include_router(jwk_router)
router.include_router(session_router)
router.include_router(app_router)
