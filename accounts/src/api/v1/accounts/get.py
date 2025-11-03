from uuid import UUID

from src.api.v1.accounts.router import router
from src.schemas import AccountSchema
from src.services import AccountsService
from package import json_encoder


@router.get('/{account_id}')
async def get_account(account_id: UUID) -> AccountSchema:
    account = await AccountsService.get_account(account_id)
    return AccountSchema.model_validate_json(json_encoder.encode(account))
