from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.delivery.http.identities.router import router
from src.contexts.authentication.delivery.http.identities.schemas import (
    CreateIdentityRequest,
    CreateIdentityResponse,
)
from src.contexts.authentication.application import IIdentityService
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_identity(
    payload: CreateIdentityRequest,
    service: IIdentityService = Depends(Provide['auth.identity_service']),
    _: AuthContext = Depends(require_auth),
) -> CreateIdentityResponse:
    identity = await service.create(
        payload.account_id,
        payload.provider_type,
        payload.credentials,
    )
    return CreateIdentityResponse(id=identity.id)
