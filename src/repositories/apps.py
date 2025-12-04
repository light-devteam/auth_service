from datetime import datetime, timezone
from uuid import UUID

from asyncpg import UniqueViolationError, Connection

from src.storages import postgres
from src.dao import AppsDAO
from src.dto import AppDTO
from src.exceptions import AppAlreadyExistsException, AppNotExistsException
from src.specifications import EqualSpecification
from src.enums import PostgresLocks


class AppsRepository:
    @classmethod
    async def create_app(
        cls,
        account_id: UUID,
        name: str,
        description: str = '',
    ) -> UUID:
        async with postgres.pool.acquire() as connection:
            app_data = {
                'account_id': account_id,
                'name': name,
                'description': description,
            }
            try:
                app = await AppsDAO.create(connection, app_data, ['id'])
            except UniqueViolationError:
                raise AppAlreadyExistsException()
            return UUID(str(app['id']))

    @classmethod
    async def get_apps(
        cls,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[AppDTO]:
        async with postgres.pool.acquire() as connection:
            apps = await AppsDAO.get(
                connection,
                ['id', 'account_id', 'name', 'description', 'created_at', 'deleted_at'],
                EqualSpecification('account_id', account_id),
                page=page,
                page_size=page_size,
            )
        return [AppDTO(**app) for app in apps]

    @classmethod
    async def get(
        cls,
        app_id: UUID,
    ) -> AppDTO:
        async with postgres.pool.acquire() as connection:
            apps = await AppsDAO.get(
                connection,
                ['id', 'account_id', 'name', 'description', 'created_at', 'deleted_at'],
                EqualSpecification('id', app_id),
            )
        if len(apps) != 1:
            raise AppNotExistsException()
        return AppDTO(**apps[0])

    @classmethod
    async def delete(cls, app_id: UUID) -> None:
        async with postgres.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                apps = await AppsDAO.get(
                    connection,
                    ['deleted_at'],
                    EqualSpecification('id', app_id),
                    lock=PostgresLocks.FOR_NO_KEY_UPDATE,
                )
                if len(apps) != 1:
                    raise AppNotExistsException()
                if apps[0]['deleted_at'] != None:
                    raise AppNotExistsException()
                await AppsDAO.update(
                    connection,
                    {'deleted_at': datetime.now(tz=timezone.utc)},
                    EqualSpecification('id', app_id),
                )
