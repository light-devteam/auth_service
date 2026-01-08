from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.contexts.authentication.domain.entities import Session
from src.contexts.authentication.domain.value_objects import ProviderType


class ISessionService(ABC):
    @abstractmethod
    async def authenticate(
        self,
        provider_type: ProviderType,
        credentials: dict[str, Any],
    ) -> Session:
        ...

    @abstractmethod
    async def create(
        self,
        provider_type: ProviderType,
        credentials: dict[str, Any],
    ) -> Session:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Session:
        ...

    @abstractmethod
    async def get_by_account_id(
        self,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[Session]:
        ...

    @abstractmethod
    async def get_by_account_id_and_provider_id(
        self,
        account_id: UUID,
        provider_id: UUID,
    ) -> Session:
        ...
