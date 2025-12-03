from uuid import UUID

from asyncpg import UniqueViolationError

from src.enums import AppTypes
from src.storages import postgres
from src.dao import AppsDAO
from src.dto import AppDTO
from src.exceptions import AppAlreadyExistsException
from src.specifications import EqualSpecification


class AppsRepository:
    @classmethod
    async def create_app(
        cls,
        account_id: UUID,
        name: str,
        type: AppTypes,
        description: str = '',
    ) -> UUID:
        async with postgres.pool.acquire() as connection:
            app_data = {
                'account_id': account_id,
                'name': name,
                'description': description,
                'type': type.value,
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
                ['id', 'account_id', 'name', 'description', 'type'],
                EqualSpecification('account_id', account_id),
                page=page,
                page_size=page_size,
            )
        return [AppDTO(**app) for app in apps]
