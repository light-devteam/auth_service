from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router
from src.contexts.authentication.delivery.http.providers.schemas import Provider
from src.contexts.authentication.domain.value_objects import ProviderType


@router.get('/type/{provider_type}')
@inject
async def get_providers_by_type(
    provider_type: ProviderType,
    page: int = 1,
    page_size: int = 100,
    service: IProviderService = Depends(Provide['auth.provider_service']),
) -> list[Provider]:
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 1
    providers = await service.get_by_type(provider_type, page, page_size)
    return [Provider(**structs.asdict(provider)) for provider in providers]
