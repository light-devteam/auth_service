from uuid import UUID

from fastapi import Depends

from package import json_encoder
from src.api.v1.app.token.router import router
from src.services import AppTokensService
from src.schemas import AppTokenMetaSchema
from src.dto import TokenPayloadDTO
from src.dependencies import get_validated_token


@router.get('')
async def get_all(
    app_id: UUID,
    token: TokenPayloadDTO = Depends(get_validated_token),
) -> list[AppTokenMetaSchema]:
    tokens = await AppTokensService.get_all(
        account_id=token.sub,
        app_id=app_id,
    )
    return [AppTokenMetaSchema.model_validate_json(json_encoder.encode(token)) for token in tokens]
