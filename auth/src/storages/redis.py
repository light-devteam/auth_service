from redis.asyncio import Redis, ConnectionPool

from src.storages.base import BaseStorage
from src.schemas import HealthCheck
from src.enums import HealthStatus
from config import settings

POOL_SIZE = 64


class RedisStorage(BaseStorage):
    async def connect(self) -> None:
        self._pool = ConnectionPool.from_url(
            url=self._db_url,
            max_connections=POOL_SIZE,
        )
        self._redis = Redis(connection_pool=self._pool)

    @property
    def pool(self) -> ConnectionPool:
        return self._pool

    @property
    def connection(self) -> Redis:
        return self._redis

    async def disconnect(self) -> None:
        await self._redis.close()
        await self._pool.aclose()

    async def healthcheck(self) -> HealthCheck:
        health_status = HealthStatus.HEALTHY
        try:
            await self._redis.ping()
        except Exception:
            health_status = HealthStatus.UNHEALTHY
        return HealthCheck(
            name='Redis healthcheck',
            status=health_status,
        )


redis = RedisStorage(settings.REDIS_URL)
