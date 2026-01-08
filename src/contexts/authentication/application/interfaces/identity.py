from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain.value_objects import ProviderType


class IIdentityService(ABC):
    @abstractmethod
    async def create(
        self,
        account_id: UUID,
        provider_type: ProviderType,
        credentials: dict[str, Any],
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
    async def get_by_account_and_provider(
        self,
        account_id: UUID,
        provider_type: ProviderType,
    ) -> Identity:
        ...
