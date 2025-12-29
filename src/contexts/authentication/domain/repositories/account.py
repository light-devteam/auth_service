from abc import ABC, abstractmethod

from src.domain import IDatabaseContext
from src.domain.value_objects.id import AccountID
from src.domain.entities import Account


class IAccountRepository(ABC):
    @abstractmethod
    async def create(
        self,
        ctx: IDatabaseContext,
        account: Account,
    ) -> None:
        ...

    @abstractmethod
    async def get_by_id(
        self,
        ctx: IDatabaseContext,
        id: AccountID,
    ) -> Account:
        ...
