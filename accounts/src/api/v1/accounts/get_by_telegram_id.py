from src.api.v1.accounts.router import router
from src.schemas import AccountSchema
from src.services import AccountsService
from package import json_encoder


@router.get('/telegram/{telegram_id}')
async def get_account(telegram_id: int) -> AccountSchema:
    account = await AccountsService.get_account_by_telegram_id(telegram_id)
    return AccountSchema.model_validate_json(json_encoder.encode(account))
