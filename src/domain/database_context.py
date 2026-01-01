from typing import Optional, TypeVar, Type, Protocol, runtime_checkable
from types import TracebackType


TConnection = TypeVar('TConnection')


@runtime_checkable
class IDatabaseContext(Protocol[TConnection]):
    _connection: TConnection

    async def __aenter__(self) -> 'IDatabaseContext[TConnection]':
        raise NotImplementedError()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        raise NotImplementedError()

    @property
    def connection(self) -> TConnection:
        raise NotImplementedError()

    async def use_transaction(self) -> None:
        raise NotImplementedError()
