import asyncpg

from src.infrastructure.persistence.base import BaseClient

MIN_POOL_SIZE = 1
MAX_POOL_SIZE = 15
MAX_POOL_QUERIES = 50000
MAX_POOL_INACTIVAE_CONNECTION_LIFETIME = 300.0


class PostgresClient(BaseClient):
    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(
            dsn=self._db_url,
            min_size=MIN_POOL_SIZE,
            max_size=MAX_POOL_SIZE,
            max_queries=MAX_POOL_QUERIES,
            max_inactive_connection_lifetime=MAX_POOL_INACTIVAE_CONNECTION_LIFETIME,
        )

    @property
    def pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError('PostgreSQL pool is not connected')
        return self._pool

    async def disconnect(self) -> None:
        await self._pool.close()
