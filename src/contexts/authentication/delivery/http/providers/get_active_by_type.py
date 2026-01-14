from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router
from src.contexts.authentication.delivery.http.providers.schemas import Provider
from src.contexts.authentication.domain.value_objects import ProviderType
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.get('/type/{provider_type}/active')
@inject
async def get_active_provider_by_type(
    provider_type: ProviderType,
    service: IProviderService = Depends(Provide['auth.provider_service']),
    _: AuthContext = Depends(require_auth),
) -> Provider:
    provider = await service.get_active_by_type(provider_type)
    return Provider(**structs.asdict(provider))
