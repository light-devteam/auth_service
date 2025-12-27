from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from src.contexts.authentication.application.services import AccountApplicationService
from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.delivery.http.accounts.schemas import CreateAccountResponse


@router.post('')
@inject
async def create_account(
    service: AccountApplicationService = Depends(Provide['accounts_application_service']),
) -> CreateAccountResponse:
    account = await service.create()
    return CreateAccountResponse(id=account.id)
