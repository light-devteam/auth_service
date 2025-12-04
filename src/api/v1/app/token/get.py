from uuid import UUID

from fastapi import Depends, HTTPException, status

from package import json_encoder
from src.api.v1.app.token.router import router
from src.services import AppTokensService
from src.schemas import AppTokenMetaSchema
from src.dto import PrincipalDTO
from src.dependencies import get_principal
from src.enums import PrincipalTypes


@router.get('/apps/tokens/{token_id}')
async def get(
    token_id: UUID,
    token: PrincipalDTO = Depends(get_principal),
) -> AppTokenMetaSchema:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    token_dto = await AppTokensService.get(token_id)
    return AppTokenMetaSchema.model_validate_json(json_encoder.encode(token_dto))
