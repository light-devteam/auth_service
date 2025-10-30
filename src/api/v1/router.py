from fastapi import APIRouter

from src.api.v1.healthcheck import router as health_router

router = APIRouter(prefix='/v1')
router.include_router(health_router)
