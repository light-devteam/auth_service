from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application import IAccountService
from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.delivery.http.accounts.schemas import Account
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.get('/{account_id}')
@inject
async def get_account(
    account_id: UUID,
    service: IAccountService = Depends(Provide['auth.accounts_service']),
    _: AuthContext = Depends(require_auth),
) -> Account:
    account = await service.get_by_id(account_id)
    return Account(id=account.id)
