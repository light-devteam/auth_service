from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router
from src.contexts.authentication.delivery.http.providers.schemas import (
    CreateProviderRequest,
    CreateProviderResponse,
)


@router.post('')
@inject
async def create_provider(
    payload: CreateProviderRequest,
    service: IProviderService = Depends(Provide['auth.provider_service']),
) -> CreateProviderResponse:
    provider = await service.create(
        payload.name,
        payload.config,
    )
    return CreateProviderResponse(id=provider.id)
