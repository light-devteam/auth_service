from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application import IIdentityService
from src.contexts.authentication.delivery.http.identities.router import router
from src.contexts.authentication.delivery.http.identities.schemas import Identity


@router.get('/{identity_id}')
@inject
async def get_identity(
    identity_id: UUID,
    service: IIdentityService = Depends(Provide['identity_application_service']),
) -> Identity:
    identity = await service.get_by_id(identity_id)
    return Identity(**structs.asdict(identity))
