from fastapi import Depends

from package import json_encoder
from src.api.v1.app.router import router
from src.services import AppsService
from src.schemas import AppSchema
from src.dto import TokenPayloadDTO
from src.dependencies import get_validated_token


@router.get('')
async def get_apps(
    page: int = 1,
    page_size: int = 100,
    token: TokenPayloadDTO = Depends(get_validated_token),
) -> list[AppSchema]:
    app_dtos = await AppsService.get_apps(
        account_id=token.sub,
        page=page,
        page_size=page_size,
    )
    return [AppSchema.model_validate_json(json_encoder.encode(app_dto)) for app_dto in app_dtos]
