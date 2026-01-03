from abc import ABC, abstractmethod

from src.domain.database_context import IDatabaseContext
from src.contexts.authentication.domain import value_objects, entities
from src.domain.value_objects import AccountID


class ISessionRepository(ABC):
    @abstractmethod
    async def create(
        self,
        ctx: IDatabaseContext,
        session: entities.Session,
    ) -> None:
        ...

    @abstractmethod
    async def get_by_id(
        self,
        ctx: IDatabaseContext,
        id: value_objects.SessionID,
    ) -> entities.Session:
        ...

    @abstractmethod
    async def get_by_account_id(
        self,
        ctx: IDatabaseContext,
        account_id: AccountID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[entities.Session]:
        ...

    @abstractmethod
    async def get_by_account_id_and_provider_id(
        self,
        ctx: IDatabaseContext,
        account_id: AccountID,
        provider_id: value_objects.ProviderID,
    ) -> entities.Session:
        ...

    @abstractmethod
    async def update(
        self,
        ctx: IDatabaseContext,
        *sessions: entities.Session,
    ) -> None:
        ...
