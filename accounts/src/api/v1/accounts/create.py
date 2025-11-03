from uuid import UUID

from src.api.v1.accounts.router import router
from src.services.accounts import AccountsService
from src.schemas import CreateAccountSchema


@router.post('/')
async def create_account(creation_data: CreateAccountSchema) -> UUID:
    return await AccountsService.create_account(creation_data.telegram_id)
