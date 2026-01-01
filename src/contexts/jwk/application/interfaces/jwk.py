from abc import ABC, abstractmethod
from uuid import UUID

from src.contexts.jwk.domain.entities import JWKToken


class IJWKService(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        id: UUID,
    ) -> JWKToken:
        ...

    @abstractmethod
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 100,
        only_active: bool = True,
    ) -> list[JWKToken]:
        ...

    @abstractmethod
    async def create(self, name: str) -> JWKToken:
        ...

    @abstractmethod
    async def toggle_active(
        self,
        id: UUID,
    ) -> JWKToken:
        ...

    @abstractmethod
    async def set_primary(
        self,
        id: UUID,
    ) -> tuple[JWKToken, JWKToken]:
        ...
