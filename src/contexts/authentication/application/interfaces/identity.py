from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.contexts.authentication.domain.entities import Identity


class IIdentityService(ABC):
    @abstractmethod
    async def create(
        self,
        account_id: UUID,
        provider_id: UUID,
        provider_data: dict[str, Any],
    ) -> Identity:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Identity:
        ...

    @abstractmethod
    async def get_by_account_id(
        self,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[Identity]:
        ...

    @abstractmethod
    async def get_by_account_id_and_provider_id(
        self,
        account_id: UUID,
        provider_id: UUID,
    ) -> Identity:
        ...
