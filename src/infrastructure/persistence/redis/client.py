from redis.asyncio import Redis, ConnectionPool

from src.domain import IDatabaseClient


POOL_SIZE = 64


class RedisClient(IDatabaseClient):
    async def connect(self) -> None:
        self._pool = ConnectionPool.from_url(
            url=self._db_url,
            max_connections=POOL_SIZE,
        )
        self._redis = Redis(connection_pool=self._pool)

    @property
    def pool(self) -> ConnectionPool:
        self.__check_pool()
        return self._pool

    @property
    def connection(self) -> Redis:
        self.__check_redis()
        return self._redis

    async def disconnect(self) -> None:
        self.__check_redis()
        await self._redis.close()
        self.__check_pool()
        await self._pool.aclose()

    def __check_redis(self) -> None:
        if not hasattr(self, '_redis') or not self._redis:
            raise RuntimeError('Redis is not connected')

    def __check_pool(self) -> None:
        if not hasattr(self, '_pool') or not self._pool:
            raise RuntimeError('Redis pool is not connected')
