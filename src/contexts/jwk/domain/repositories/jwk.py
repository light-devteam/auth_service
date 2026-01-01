from uuid import UUID
from abc import ABC, abstractmethod

from src.domain import IDatabaseContext
from src.contexts.jwk.domain.entities import JWKToken
from src.contexts.jwk.domain.value_objects import JWKTokenID


class IJWKRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        ctx: IDatabaseContext,
        id: JWKTokenID,
    ) -> JWKToken:
        ...

    @abstractmethod
    async def get_primary(self, ctx: IDatabaseContext) -> JWKToken:
        ...

    @abstractmethod
    async def get_all(
        self,
        ctx: IDatabaseContext,
        page: int = 1,
        page_size: int = 100,
        only_active: bool = True,
    ) -> list[JWKToken]:
        ...

    @abstractmethod
    async def create(
        self,
        ctx: IDatabaseContext,
        jwk: JWKToken,
    ) -> None:
        ...

    @abstractmethod
    async def update(
        self,
        ctx: IDatabaseContext,
        *jwk_tokens: JWKToken,
    ) -> None:
        ...
