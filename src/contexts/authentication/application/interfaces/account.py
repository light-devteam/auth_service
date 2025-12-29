from abc import ABC, abstractmethod

from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.entities import Account


class IAccountService(ABC):
    @abstractmethod
    async def create(self) -> Account:
        ...

    @abstractmethod
    async def get_by_id(self, id: AccountID) -> Account:
        ...
