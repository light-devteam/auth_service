from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application import IIdentityService
from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.delivery.http.identities.schemas import Identity


@router.get('/{account_id}/identities/by-provider/{provider_id}')
@inject
async def get_account_identity_by_provider_id(
    account_id: UUID,
    provider_id: UUID,
    service: IIdentityService = Depends(Provide['auth.identity_service']),
) -> Identity:
    identity = await service.get_by_account_id_and_provider_id(account_id, provider_id)
    return Identity(**structs.asdict(identity))
