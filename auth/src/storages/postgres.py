import asyncpg

from config import settings
from src.storages.base import BaseStorage
from src.schemas import HealthCheck
from src.enums import HealthStatus

MIN_POOL_SIZE = 1
MAX_POOL_SIZE = 15
MAX_POOL_QUERIES = 50000
MAX_POOL_INACTIVAE_CONNECTION_LIFETIME = 300.0


class PostgresStorage(BaseStorage):
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
        return self._pool

    async def disconnect(self) -> None:
        await self._pool.close()

    async def healthcheck(self) -> HealthCheck:
        async with self.pool.acquire() as db:
            db: asyncpg.Connection
            health_status = HealthStatus.HEALTHY
            try:
                await db.fetchval('select 1')
            except Exception:
                health_status = HealthStatus.UNHEALTHY
            return HealthCheck(
                name='PostgreSQL healthcheck',
                status=health_status,
            )


postgres = PostgresStorage(settings.POSTGRES_URL)
