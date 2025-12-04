from fastapi import Depends, HTTPException, status

from src.api.v1.app.router import router
from src.services import AppsService
from src.schemas import CreateAppRequestSchema, CreateAppResponseSchema
from src.dto import PrincipalDTO
from src.dependencies import get_principal
from src.enums import PrincipalTypes


@router.post('/apps')
async def create(
    creation_data: CreateAppRequestSchema,
    token: PrincipalDTO = Depends(get_principal),
) -> CreateAppResponseSchema:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    app_id = await AppsService.create_app(
        account_id=creation_data.account_id,
        name=creation_data.name,
        description=creation_data.description,
    )
    return CreateAppResponseSchema(id=app_id)
