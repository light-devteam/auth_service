from uuid import UUID

from fastapi import Depends, HTTPException, status

from package import json_encoder
from src.api.v1.app.router import router
from src.services import AppsService
from src.schemas import AppSchema
from src.dto import PrincipalDTO
from src.dependencies import get_principal
from src.enums import PrincipalTypes


@router.get('/apps/{app_id}')
async def get(
    app_id: UUID,
    token: PrincipalDTO = Depends(get_principal),
) -> AppSchema:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    app_dto = await AppsService.get(app_id)
    return AppSchema.model_validate_json(json_encoder.encode(app_dto))
