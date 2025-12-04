from datetime import datetime, timezone
from uuid import UUID

from asyncpg import UniqueViolationError, Connection

from src.storages import postgres
from src.dao import AppTokensDAO, AppsDAO
from src.exceptions import (
    TokenAlreadyExistsException,
    TokenNotExistsException,
    InvalidTokenException,
    AppNotExistsException,
)
from src.specifications import EqualSpecification, IsNullSpecification
from src.dto import AppTokenMetaDTO, AppTokenValidationInfoDTO
from src.enums import PostgresLocks


class AppTokensRepository:
    @classmethod
    async def create_token(
        cls,
        app_id: UUID,
        name: str,
        hash: str,
        expires_at: datetime | None = None,
    ) -> UUID:
        async with postgres.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                await cls.__filter_deleted_apps(connection, app_id)
                token_data = {
                    'app_id': app_id,
                    'name': name,
                    'hash': hash,
                    'expires_at': expires_at,
                }
                try:
                    token = await AppTokensDAO.create(connection, token_data, ['id'])
                except UniqueViolationError:
                    raise TokenAlreadyExistsException()
                return UUID(str(token['id']))

    @classmethod
    async def get_all(
        cls,
        app_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[AppTokenMetaDTO]:
        async with postgres.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                await cls.__filter_deleted_apps(connection, app_id)
                tokens = await AppTokensDAO.get(
                    connection,
                    ['id', 'app_id', 'name', 'created_at', 'expires_at', 'revoked_at'],
                    EqualSpecification('app_id', app_id),
                    page=page,
                    page_size=page_size,
                )
                return [AppTokenMetaDTO(**token) for token in tokens]

    @classmethod
    async def get(
        cls,
        token_id: UUID,
    ) -> AppTokenMetaDTO:
        async with postgres.pool.acquire() as connection:
            tokens = await AppTokensDAO.get(
                connection,
                ['id', 'app_id', 'name', 'created_at', 'expires_at', 'revoked_at'],
                EqualSpecification('id', token_id),
                IsNullSpecification('revoked_at'),
            )
            if len(tokens) != 1:
                raise TokenNotExistsException()
            return AppTokenMetaDTO(**tokens[0])

    @classmethod
    async def revoke(cls, token_id: UUID) -> None:
        async with postgres.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                tokens = await AppTokensDAO.get(
                    connection,
                    ['revoked_at'],
                    EqualSpecification('id', token_id),
                    lock=PostgresLocks.FOR_NO_KEY_UPDATE,
                )
                if len(tokens) != 1:
                    raise TokenNotExistsException()
                if tokens[0]['revoked_at'] != None:
                    raise TokenNotExistsException()
                await AppTokensDAO.update(
                    connection,
                    {'revoked_at': datetime.now(tz=timezone.utc)},
                    EqualSpecification('id', token_id),
                )

    @classmethod
    async def get_validation_info(cls, token_id: UUID) -> AppTokenValidationInfoDTO:
        async with postgres.pool.acquire() as connection:
            tokens = await AppTokensDAO.get(
                connection,
                ['app_id', 'hash'],
                EqualSpecification('id', token_id),
            )
            if len(tokens) != 1:
                raise InvalidTokenException()
            token = tokens[0]
            return AppTokenValidationInfoDTO(
                app_id=UUID(str(token['app_id'])),
                hash=token['hash'],
            )

    @classmethod
    async def __filter_deleted_apps(connection: Connection, app_id: UUID) -> None:
        apps = await AppsDAO.get(
            connection,
            ['deleted_at'],
            EqualSpecification('id', app_id),
            lock=PostgresLocks.FOR_KEY_SHARE,
        )
        if len(apps) != 1:
            raise AppNotExistsException()
        if apps[0]['deleted_at'] != None:
            raise AppNotExistsException()
