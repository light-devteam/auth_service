from fastapi import Depends

from src.api.v1.session.router import router
from src.dependencies import get_validated_token


@router.get('/auth')
async def auth(token: str = Depends(get_validated_token)) -> None:
    return
