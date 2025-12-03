from fastapi import APIRouter

from src.api.v1.app.token import router as token_router


router = APIRouter(
    prefix='/app',
    tags=['Apps'],
)
router.include_router(token_router)
