from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import Account


class IAccountService(ABC):
    @abstractmethod
    async def create(self) -> Account:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Account:
        ...
