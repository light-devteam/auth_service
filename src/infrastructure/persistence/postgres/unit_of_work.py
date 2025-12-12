from typing import Optional, Type
from types import TracebackType

from asyncpg import Connection, transaction

from src.domain import IDatabaseContext
from src.infrastructure.persistence.postgres.client import PostgresClient


class PostgresUnitOfWork(IDatabaseContext[Connection]):
    def __init__(self, client: PostgresClient) -> None:
        self._client = client
        self._connection: Connection | None = None
        self._transaction: transaction.Transaction | None = None

    async def __aenter__(self) -> 'PostgresUnitOfWork[Connection]':
        self._connection = await self._client.pool.acquire()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._transaction is not None:
            await self._transaction.__aexit__(exc_type, exc_value, traceback)
            self._transaction = None
        if self._connection is not None:
            await self._client.pool.release(self._connection)
            self._connection = None

    @property
    def connection(self) -> Connection:
        self.__check_connection()
        return self._connection

    async def use_transaction(self) -> None:
        self.__check_connection()
        self._transaction = self._connection.transaction()
        await self._transaction.__aenter__()

    def __check_connection(self) -> None:
        if not hasattr(self, '_connection') or self._connection is None:
            raise RuntimeError('Connection not exists')
