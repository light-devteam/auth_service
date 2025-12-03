from uuid import UUID

from asyncpg import UniqueViolationError

from src.storages import postgres
from src.dao import AppTokensDAO
from src.exceptions import TokenAlreadyExistsException


class AppTokensRepository:
    @classmethod
    async def create_token(
        cls,
        app_id: UUID,
        name: str,
        hash: str,
    ) -> None:
        async with postgres.pool.acquire() as connection:
            token_data = {
                'app_id': app_id,
                'name': name,
                'hash': hash,
            }
            try:
                await AppTokensDAO.create(connection, token_data)
            except UniqueViolationError:
                raise TokenAlreadyExistsException()
