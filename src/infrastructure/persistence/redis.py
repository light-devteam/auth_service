from redis.asyncio import Redis, ConnectionPool

from src.infrastructure.persistence.base import BaseClient


POOL_SIZE = 64


class RedisClient(BaseClient):
    async def connect(self) -> None:
        self._pool = ConnectionPool.from_url(
            url=self._db_url,
            max_connections=POOL_SIZE,
        )
        self._redis = Redis(connection_pool=self._pool)

    @property
    def pool(self) -> ConnectionPool:
        if self._pool is None:
            raise RuntimeError('Redis pool is not connected')
        return self._pool

    @property
    def connection(self) -> Redis:
        return self._redis

    async def disconnect(self) -> None:
        await self._redis.close()
        await self._pool.aclose()
