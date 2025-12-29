from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application import IAccountService
from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.delivery.http.accounts.schemas import Account


@router.get(
    '/{account_id}',
    response_model_exclude_unset=True,
)
@inject
async def get_account(
    account_id: UUID,
    service: IAccountService = Depends(Provide['accounts_application_service']),
) -> Account:
    account = await service.get_by_id(account_id)
    return Account(id=account.id)
