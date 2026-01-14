from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router
from src.contexts.authentication.delivery.http.providers.schemas import Provider
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.get('/{provider_id}')
@inject
async def get_provider(
    provider_id: UUID,
    service: IProviderService = Depends(Provide['auth.provider_service']),
    _: AuthContext = Depends(require_auth),
) -> Provider:
    provider = await service.get_by_id(provider_id)
    return Provider(**structs.asdict(provider))
