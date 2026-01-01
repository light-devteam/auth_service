from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from msgspec import structs

from src.contexts.authentication.application import IIdentityService
from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.delivery.http.identities.schemas import Identity


@router.get('/{account_id}/identities')
@inject
async def get_account_identities(
    account_id: UUID,
    page: int = 1,
    page_size: int = 100,
    service: IIdentityService = Depends(Provide['identity_application_service']),
) -> list[Identity]:
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 1
    identities = await service.get_by_account_id(account_id, page, page_size)
    return [Identity(**structs.asdict(identity)) for identity in identities]
