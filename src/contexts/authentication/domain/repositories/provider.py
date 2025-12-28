from abc import ABC, abstractmethod

from src.domain.database_context import IDatabaseContext
from src.contexts.authentication.domain import value_objects, entities


class IProviderRepository(ABC):
    @abstractmethod
    async def create(
        self,
        ctx: IDatabaseContext,
        provider: entities.Provider,
    ) -> None:
        ...

    @abstractmethod
    async def get_by_id(
        self,
        ctx: IDatabaseContext,
        id: value_objects.ProviderID,
    ) -> entities.Provider:
        ...

    @abstractmethod
    async def update(
        self,
        ctx: IDatabaseContext,
        *providers: entities.Provider,
    ) -> None:
        ...
