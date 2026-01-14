from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application import IIdentityService
from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.delivery.http.identities.schemas import Identity
from src.contexts.authentication.domain.value_objects import ProviderType, AuthContext
from src.delivery.dependencies import require_auth


@router.get('/{account_id}/identities/by-provider/{provider_type}')
@inject
async def get_account_identity_by_provider(
    account_id: UUID,
    provider_type: ProviderType,
    service: IIdentityService = Depends(Provide['auth.identity_service']),
    _: AuthContext = Depends(require_auth),
) -> Identity:
    identity = await service.get_by_account_and_provider(account_id, provider_type)
    return Identity(**structs.asdict(identity))
