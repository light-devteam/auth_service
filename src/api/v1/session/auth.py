from fastapi import Depends

from src.api.v1.session.router import router
from src.dependencies import get_principal
from src.dto import PrincipalDTO


@router.get('/auth')
async def auth(token: PrincipalDTO = Depends(get_principal)) -> None:
    return
