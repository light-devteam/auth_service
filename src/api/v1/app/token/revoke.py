from uuid import UUID

from fastapi import Depends, HTTPException, status

from src.api.v1.app.token.router import router
from src.services import AppTokensService
from src.dto import PrincipalDTO
from src.dependencies import get_principal
from src.enums import PrincipalTypes


@router.delete(
    '/apps/tokens/{token_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def revoke(
    token_id: UUID,
    token: PrincipalDTO = Depends(get_principal),
) -> None:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await AppTokensService.revoke(token_id)
