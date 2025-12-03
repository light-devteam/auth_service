from fastapi import Depends, HTTPException, status

from package import json_encoder
from src.api.v1.app.router import router
from src.services import AppsService
from src.schemas import AppSchema
from src.dto import PrincipalDTO
from src.dependencies import get_principal
from src.enums import PrincipalTypes


@router.get('')
async def get_apps(
    page: int = 1,
    page_size: int = 100,
    token: PrincipalDTO = Depends(get_principal),
) -> list[AppSchema]:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    app_dtos = await AppsService.get_apps(
        account_id=token.id,
        page=page,
        page_size=page_size,
    )
    return [AppSchema.model_validate_json(json_encoder.encode(app_dto)) for app_dto in app_dtos]
