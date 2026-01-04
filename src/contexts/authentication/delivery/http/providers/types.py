from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router


@router.get('/types')
@inject
async def get_providers_types(
    service: IProviderService = Depends(Provide['auth.provider_service']),
) -> list[str]:
    return await service.get_types()
