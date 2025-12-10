from fastapi import APIRouter

from src.system.delivery.http.health import router as health_router


router = APIRouter(prefix='/health')
router.include_router(health_router)
