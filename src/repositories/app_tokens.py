from uuid import UUID

from asyncpg import Connection, UniqueViolationError

from src.storages import postgres
from src.dao import AppTokensDAO, AppsDAO
from src.exceptions import TokenAlreadyExistsException, AppNotExistsException
from src.specifications import EqualSpecification
from src.dto import AppTokenMetaDTO


class AppTokensRepository:
    @classmethod
    async def create_token(
        cls,
        account_id: UUID,
        app_id: UUID,
        name: str,
        hash: str,
    ) -> UUID:
        async with postgres.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                account_apps = await AppsDAO.get(
                    connection,
                    ['id'],
                    EqualSpecification('a.account_id', account_id),
                    EqualSpecification('a.id', app_id),
                )
                if len(account_apps) != 1:
                    raise AppNotExistsException()
                token_data = {
                    'app_id': app_id,
                    'name': name,
                    'hash': hash,
                }
                try:
                    token = await AppTokensDAO.create(connection, token_data, ['id'])
                except UniqueViolationError:
                    raise TokenAlreadyExistsException()
                return UUID(str(token['id']))

    @classmethod
    async def get_all(cls, account_id: UUID, app_id: UUID) -> list[AppTokenMetaDTO]:
        async with postgres.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                account_apps = await AppsDAO.get(
                    connection,
                    ['id'],
                    EqualSpecification('a.account_id', account_id),
                    EqualSpecification('a.id', app_id),
                )
                if len(account_apps) != 1:
                    raise AppNotExistsException()
                tokens = await AppTokensDAO.get(
                    connection,
                    ['id', 'app_id', 'name', 'created_at'],
                    EqualSpecification('app_id', app_id)
                )
                return (AppTokenMetaDTO(**token) for token in tokens)
