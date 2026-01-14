from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router
from src.contexts.authentication.delivery.http.providers.schemas import (
    CreateProviderRequest,
    CreateProviderResponse,
)
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.post('')
@inject
async def create_provider(
    payload: CreateProviderRequest,
    service: IProviderService = Depends(Provide['auth.provider_service']),
    _: AuthContext = Depends(require_auth),
) -> CreateProviderResponse:
    provider = await service.create(
        payload.name,
        payload.type,
        payload.config,
    )
    return CreateProviderResponse(id=provider.id)
