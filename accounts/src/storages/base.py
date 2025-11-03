from abc import ABC, abstractmethod


class BaseStorage(ABC):
    def __init__(self, db_url: str) -> None:
        self._db_url = db_url

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def healthcheck(self) -> None:
        raise NotImplementedError()
