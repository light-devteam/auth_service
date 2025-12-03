from uuid import UUID

from fastapi import Depends

from src.api.v1.app.token.router import router
from src.services import AppTokensService
from src.schemas import CreateTokenRequestSchema, CreateTokenResponseSchema
from src.dto import TokenPayloadDTO
from src.dependencies import get_validated_token


@router.post('')
async def create(
    app_id: UUID,
    creation_data: CreateTokenRequestSchema,
    token: TokenPayloadDTO = Depends(get_validated_token),
) -> CreateTokenResponseSchema:
    api_token = await AppTokensService.create_token(
        account_id=token.sub,
        app_id=app_id,
        name=creation_data.name,
    )
    return CreateTokenResponseSchema(token=api_token)
