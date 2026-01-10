from abc import ABC, abstractmethod

from src.domain.database_context import IDatabaseContext
from src.contexts.authentication.domain import value_objects, entities


class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def create(
        self,
        ctx: IDatabaseContext,
        refresh_token: entities.RefreshToken,
    ) -> None:
        ...

    @abstractmethod
    async def get_by_id(
        self,
        ctx: IDatabaseContext,
        id: value_objects.RefreshTokenID,
    ) -> entities.RefreshToken:
        ...
