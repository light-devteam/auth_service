from uuid import UUID

from asyncpg import UniqueViolationError

from src.dao import AccountsDAO
from src.storages import postgres
from src.specifications import EqualSpecification
from src.dto import AccountDTO
from src.exceptions import AccountNotFoundException, AccountAlreadyExistsException


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

    @classmethod
    async def get_all(cls, page: int = 1, page_size: int = 100) -> list[AccountDTO]:
        async with postgres.pool.acquire() as connection:
            account_records = await AccountsDAO.get(
                connection,
                ['id, telegram_id'],
                page=page,
                page_size=page_size,
            )
        return [AccountDTO(**account_record) for account_record in account_records]

    @classmethod
    async def create_account(cls, telegram_id: int) -> UUID:
        async with postgres.pool.acquire() as connection:
            try:
                accounts_data = await AccountsDAO.create(
                    connection,
                    {'telegram_id': telegram_id},
                    ['id'],
                )
            except UniqueViolationError:
                raise AccountAlreadyExistsException()
        return UUID(str(accounts_data['id']))
