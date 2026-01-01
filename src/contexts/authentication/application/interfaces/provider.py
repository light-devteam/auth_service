from abc import ABC, abstractmethod
from typing import Any

from src.contexts.authentication.domain.entities import Provider
from src.contexts.authentication.domain.value_objects import ProviderID


class IProviderService(ABC):
    @abstractmethod
    async def create(
        self,
        name: str,
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
    async def get_by_id(self, id: ProviderID) -> Provider:
        ...

    @abstractmethod
    async def toggle_active(self, id: ProviderID) -> bool:
        ...
