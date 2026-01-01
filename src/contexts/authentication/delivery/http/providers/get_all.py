from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router
from src.contexts.authentication.delivery.http.providers.schemas import Provider


@router.get('')
@inject
async def get_all_providers(
    page: int = 1,
    page_size: int = 100,
    only_active: bool = True,
    service: IProviderService = Depends(Provide['auth.provider_service']),
) -> list[Provider]:
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 1
    providers = await service.get_all(page, page_size, only_active)
    return [Provider(**structs.asdict(provider)) for provider in providers]
