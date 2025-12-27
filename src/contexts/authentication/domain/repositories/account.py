from abc import ABC, abstractmethod

from src.domain.repositories import IAccountRepository as IAccountWithoutIdentitiesRepo
from src.domain import IDatabaseContext
from src.domain.value_objects.id import AccountID
from src.domain.entities import Account


class IAccountRepository(IAccountWithoutIdentitiesRepo, ABC):
    @abstractmethod
    async def get_by_id_with_identities(
        self,
        ctx: IDatabaseContext,
        id: AccountID,
    ) -> Account:
        ...
