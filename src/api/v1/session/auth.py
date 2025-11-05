from fastapi import Depends

from src.api.v1.session.router import router
from src.dependencies import get_validated_token
from src.dto import TokenPayloadDTO


@router.get('/auth')
async def auth(token: TokenPayloadDTO = Depends(get_validated_token)) -> None:
    return
