from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application import IAccountService
from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.delivery.http.accounts.schemas import CreateAccountResponse


@router.post('')
@inject
async def create_account(
    service: IAccountService = Depends(Provide['auth.accounts_service']),
) -> CreateAccountResponse:
    account = await service.create()
    return CreateAccountResponse(id=account.id)
