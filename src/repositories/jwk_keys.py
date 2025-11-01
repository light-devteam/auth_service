from uuid import UUID

from asyncpg import UniqueViolationError
import msgspec

from src.dao import JWKeysDAO
from src.storages import postgres
from src.specifications import EqualSpecification
from src.exceptions import JWKNotFoundException, JWKAlreadyExistsException
from src.dto import JWKInfoDTO, JWKSDTO


class JWKeysRepository:
    @classmethod
    async def get_key(cls, id: UUID) -> JWKInfoDTO:
        async with postgres.pool.acquire() as connection:
            keys = await JWKeysDAO.get(
                connection,
                ['id', 'name', 'is_active', 'created_at'],
                EqualSpecification('id', id),
            )
        if not keys:
            raise JWKNotFoundException()
        return JWKInfoDTO(**keys[0])

    @classmethod
    async def get_keys(cls, page: int = 1, page_size: int = 100) -> list[JWKInfoDTO]:
        async with postgres.pool.acquire() as connection:
            keys = await JWKeysDAO.get(
                connection,
                ['id', 'name', 'is_active', 'created_at'],
                page=page,
                page_size=page_size,
            )
        return [JWKInfoDTO(**key) for key in keys]

    @classmethod
    async def get_active_keys(cls, page: int = 1, page_size: int = 100) -> list[JWKInfoDTO]:
        async with postgres.pool.acquire() as connection:
            keys = await JWKeysDAO.get(
                connection,
                ['id', 'name', 'is_active', 'created_at'],
                EqualSpecification('is_active', True),
                page=page,
                page_size=page_size,
            )
        return [JWKInfoDTO(**key) for key in keys]

    @classmethod
    async def create_key(cls, id: UUID, name: str, public: str, private: str) -> UUID:
        async with postgres.pool.acquire() as connection:
            key_data = {
                'id': id,
                'name': name,
                'public': public,
                'private': private,
            }
            try:
                key = await JWKeysDAO.create(connection, key_data, ['id'])
            except UniqueViolationError:
                raise JWKAlreadyExistsException()
        return UUID(str(key['id']))

    @classmethod
    async def deactivate_key(cls, id: UUID) -> None:
        async with postgres.pool.acquire() as connection:
            await JWKeysDAO.update(
                connection,
                {'is_active': False},
                EqualSpecification('id', id),
                EqualSpecification('is_active', True),
            )

    @classmethod
    async def activate_key(cls, id: UUID) -> None:
        async with postgres.pool.acquire() as connection:
            await JWKeysDAO.update(
                connection,
                {'is_active': True},
                EqualSpecification('id', id),
                EqualSpecification('is_active', False),
            )

    @classmethod
    async def get_jwks(cls, page: int = 1, page_size: int = 100) -> JWKSDTO:
        async with postgres.pool.acquire() as connection:
            jwks = await JWKeysDAO.get_jwks(connection, page=page, page_size=page_size)
        return msgspec.json.decode(jwks, type=JWKSDTO)
