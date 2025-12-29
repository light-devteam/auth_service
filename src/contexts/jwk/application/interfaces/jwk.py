from abc import ABC, abstractmethod

from src.contexts.jwk.domain import entities, value_objects


class IJWKService(ABC):
    @abstractmethod
    async def get_by_id(
        self,
        id: value_objects.JWKTokenID,
    ) -> entities.JWKToken:
        ...

    @abstractmethod
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 100,
        only_active: bool = True,
    ) -> list[entities.JWKToken]:
        ...

    @abstractmethod
    async def create(self, name: str) -> entities.JWKToken:
        ...

    @abstractmethod
    async def toggle_active(
        self,
        id: value_objects.JWKTokenID,
    ) -> entities.JWKToken:
        ...

    @abstractmethod
    async def set_primary(
        self,
        id: value_objects.JWKTokenID,
    ) -> tuple[entities.JWKToken, entities.JWKToken]:
        ...
