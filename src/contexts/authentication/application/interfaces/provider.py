from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.contexts.authentication.domain.entities import Provider


class IProviderService(ABC):
    @abstractmethod
    async def create(
        self,
        name: str,
        type: str,
        config: dict[str, Any] | None = None,
    ) -> Provider:
        ...

    @abstractmethod
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 100,
        only_active: bool = True,
    ) -> list[Provider]:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Provider:
        ...

    @abstractmethod
    async def get_by_type(
        self,
        type: str,
        page: int = 1,
        page_size: int = 100,
    ) -> list[Provider]:
        ...

    @abstractmethod
    async def get_active_by_type(
        self,
        type: str,
    ) -> Provider:
        ...

    @abstractmethod
    async def activate(self, id: UUID) -> tuple[Provider, Provider | None]:
        ...

    @abstractmethod
    async def get_types(self) -> list[str]:
        ...
