from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application.services import ProviderApplicationService
from src.contexts.authentication.delivery.http.providers.router import router
from src.contexts.authentication.delivery.http.providers.schemas import ToggleActiveResponse


@router.patch('/{provider_id}/toggle_active')
@inject
async def toggle_active_state(
    provider_id: UUID,
    service: ProviderApplicationService = Depends(Provide['provider_application_service']),
) -> ToggleActiveResponse:
    current_state = await service.toggle_active(provider_id)
    return ToggleActiveResponse(is_active=current_state)
