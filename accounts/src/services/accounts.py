from uuid import UUID

from src.dto import AccountDTO
from src.repositories import AccountsRepository


class AccountsService:
    @classmethod
    async def get_account(cls, account_id: UUID) -> AccountDTO:
        return await AccountsRepository.get_account(account_id)

    @classmethod
    async def get_account_by_telegram_id(cls, telegram_id: int) -> AccountDTO:
        return await AccountsRepository.get_account_by_telegram_id(telegram_id)
