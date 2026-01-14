from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application import IIdentityService
from src.contexts.authentication.delivery.http.identities.router import router
from src.contexts.authentication.delivery.http.identities.schemas import Identity
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.get('/{identity_id}')
@inject
async def get_identity(
    identity_id: UUID,
    service: IIdentityService = Depends(Provide['auth.identity_service']),
    _: AuthContext = Depends(require_auth),
) -> Identity:
    identity = await service.get_by_id(identity_id)
    return Identity(**structs.asdict(identity))
