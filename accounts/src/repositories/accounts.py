from uuid import UUID

from src.dao import AccountsDAO
from src.storages import postgres
from src.specifications import EqualSpecification
from src.dto import AccountDTO
from src.exceptions import AccountNotFoundException


class AccountsRepository:
    @classmethod
    async def get_account(cls, account_id: UUID) -> AccountDTO:
        async with postgres.pool.acquire() as connection:
            account_records = await AccountsDAO.get(
                connection,
                ['id, telegram_id'],
                EqualSpecification('id', account_id),
            )
        if not account_records:
            raise AccountNotFoundException()
        account_record = account_records[0]
        return AccountDTO(**account_record)

    @classmethod
    async def get_account_by_telegram_id(cls, telegram_id: int) -> AccountDTO:
        async with postgres.pool.acquire() as connection:
            account_records = await AccountsDAO.get(
                connection,
                ['id, telegram_id'],
                EqualSpecification('telegram_id', telegram_id),
            )
        if not account_records:
            raise AccountNotFoundException()
        account_record = account_records[0]
        return AccountDTO(**account_record)
