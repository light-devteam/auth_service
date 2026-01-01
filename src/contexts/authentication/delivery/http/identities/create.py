from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.delivery.http.identities.router import router
from src.contexts.authentication.delivery.http.identities.schemas import (
    CreateIdentityRequest,
    CreateIdentityResponse,
)
from src.contexts.authentication.application import IIdentityService


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_identity(
    payload: CreateIdentityRequest,
    service: IIdentityService = Depends(Provide['identity_application_service'])
) -> CreateIdentityResponse:
    identity = await service.create(
        payload.account_id,
        payload.provider_id,
        payload.provider_data,
    )
    return CreateIdentityResponse(id=identity.id)
