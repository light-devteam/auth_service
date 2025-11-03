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

    @classmethod
    async def create_account(cls, telegram_id: int) -> UUID:
        return await AccountsRepository.create_account(telegram_id)

    @classmethod
    async def get_all(cls, page: int = 1, page_size: int = 100) -> list[AccountDTO]:
        return await AccountsRepository.get_all(page, page_size)
