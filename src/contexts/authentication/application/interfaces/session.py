from abc import ABC, abstractmethod
from uuid import UUID

from src.contexts.authentication.domain.entities import Session
from src.contexts.authentication.domain.value_objects import ProviderType


class ISessionService(ABC):
    @abstractmethod
    async def create(
        self,
        account_id: UUID,
        provider_type: ProviderType,
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
    async def get_by_account_and_provider(
        self,
        account_id: UUID,
        provider_type: ProviderType,
    ) -> Session:
        ...

    @abstractmethod
    async def revoke(
        self,
        session_id: UUID,
    ) -> None:
        ...
