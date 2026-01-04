from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application import IProviderService
from src.contexts.authentication.delivery.http.providers.router import router
from src.contexts.authentication.delivery.http.providers.schemas import ActivateResponse, ActiveState


@router.patch('/{provider_id}/activate')
@inject
async def activate_provider(
    provider_id: UUID,
    service: IProviderService = Depends(Provide['auth.provider_service']),
) -> ActivateResponse:
    new, old = await service.activate(provider_id)
    return ActivateResponse(
        new=ActiveState(id=new.id, is_active=new.is_active),
        old=ActiveState(id=old.id, is_active=old.is_active),
    )
