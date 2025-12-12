from fastapi import APIRouter

from src.contexts.system.delivery.http import  health_router


router = APIRouter(prefix='/health')
router.include_router(health_router)
