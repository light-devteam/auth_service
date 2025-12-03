from fastapi import Depends

from src.api.v1.app.router import router
from src.services import AppsService
from src.schemas import CreateAppRequestSchema, CreateAppResponseSchema
from src.dto import TokenPayloadDTO
from src.dependencies import get_validated_token


@router.post('')
async def create(
    creation_data: CreateAppRequestSchema,
    token: TokenPayloadDTO = Depends(get_validated_token),
) -> CreateAppResponseSchema:
    app_id = await AppsService.create_app(
        account_id=token.sub,
        name=creation_data.name,
        type=creation_data.type,
        description=creation_data.description,
    )
    return CreateAppResponseSchema(id=app_id)
