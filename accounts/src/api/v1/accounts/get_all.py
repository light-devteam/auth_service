from src.api.v1.accounts.router import router
from src.services import AccountsService
from src.schemas import AccountSchema
from package import json_encoder

@router.get('/')
async def get_all(page: int = 1, page_size: int = 100) -> list[AccountSchema]:
    accounts = await AccountsService.get_all(page, page_size)
    return [
        AccountSchema.model_validate_json(
            json_encoder.encode(account)
        ) for account in accounts
    ]
