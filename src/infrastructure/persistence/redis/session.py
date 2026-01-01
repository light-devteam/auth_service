from typing import Optional, Type
from types import TracebackType

from redis.asyncio import Redis

from src.domain import IDatabaseContext
from src.infrastructure.persistence.redis.client import RedisClient


class RedisSession(IDatabaseContext[Redis]):
    def __init__(self, client: RedisClient) -> None:
        self._client = client
        self._connection: Redis | None = None

    async def __aenter__(self) -> 'RedisSession[Redis]':
        self._connection = self._client.connection
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self._connection = None

    @property
    def connection(self) -> Redis:
        self.__check_connection()
        return self._connection

    def __check_connection(self) -> None:
        if not hasattr(self, '_connection') or self._connection is None:
            raise RuntimeError('Connection not exists')

    async def use_transaction(self) -> None:
        raise NotImplementedError()
