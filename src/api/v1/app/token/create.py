from uuid import UUID

from fastapi import Depends, HTTPException, status

from src.api.v1.app.token.router import router
from src.services import AppTokensService
from src.schemas import CreateTokenRequestSchema, CreateTokenResponseSchema
from src.dto import PrincipalDTO
from src.dependencies import get_principal
from src.enums import PrincipalTypes


@router.post('')
async def create(
    app_id: UUID,
    creation_data: CreateTokenRequestSchema,
    token: PrincipalDTO = Depends(get_principal),
) -> CreateTokenResponseSchema:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    api_token = await AppTokensService.create_token(
        account_id=token.id,
        app_id=app_id,
        name=creation_data.name,
    )
    return CreateTokenResponseSchema(token=api_token)
