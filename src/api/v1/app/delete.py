from uuid import UUID

from fastapi import Depends, HTTPException, status

from src.api.v1.app.router import router
from src.services import AppsService
from src.dto import PrincipalDTO
from src.dependencies import get_principal
from src.enums import PrincipalTypes


@router.delete(
    '/apps/{app_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    app_id: UUID,
    token: PrincipalDTO = Depends(get_principal),
) -> None:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await AppsService.delete(app_id)
