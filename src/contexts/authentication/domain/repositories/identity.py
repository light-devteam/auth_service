from abc import ABC, abstractmethod

from src.domain.database_context import IDatabaseContext
from src.contexts.authentication.domain import value_objects, entities
from src.domain.value_objects import AccountID


class IIdentityRepository(ABC):
    @abstractmethod
    async def create(
        self,
        ctx: IDatabaseContext,
        identity: entities.Identity,
    ) -> None:
        ...

    @abstractmethod
    async def get_by_id(
        self,
        ctx: IDatabaseContext,
        id: value_objects.IdentityID,
    ) -> entities.Identity:
        ...

    @abstractmethod
    async def get_by_account_id(
        self,
        ctx: IDatabaseContext,
        id: AccountID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[entities.Identity]:
        ...

    @abstractmethod
    async def get_by_account_id_and_provider_id(
        self,
        ctx: IDatabaseContext,
        account_id: AccountID,
        provider_id: value_objects.ProviderID,
    ) -> entities.Identity:
        ...

    @abstractmethod
    async def update(
        self,
        ctx: IDatabaseContext,
        *identities: entities.Identity,
    ) -> None:
        ...
