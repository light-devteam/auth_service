from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router
from src.contexts.authentication.delivery.http.providers.schemas import ActivateResponse, ActiveState
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.patch('/{provider_id}/activate')
@inject
async def activate_provider(
    provider_id: UUID,
    service: IProviderService = Depends(Provide['auth.provider_service']),
    _: AuthContext = Depends(require_auth),
) -> ActivateResponse:
    new, old = await service.activate(provider_id)
    if old:
        old_state = ActiveState(id=old.id, is_active=old.is_active)
    else:
        old_state = None
    return ActivateResponse(
        new=ActiveState(id=new.id, is_active=new.is_active),
        old=old_state,
    )
