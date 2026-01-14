from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.get('/types')
@inject
async def get_providers_types(
    service: IProviderService = Depends(Provide['auth.provider_service']),
    _: AuthContext = Depends(require_auth),
) -> list[str]:
    return await service.get_types()
