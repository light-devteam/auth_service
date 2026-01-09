from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.domain.entities import Account
from src.contexts.authentication.domain.value_objects import ProviderType


class IAccountService(ABC):
    @abstractmethod
    async def create(self) -> Account:
        ...

    @abstractmethod
    async def authenticate(
        self,
        provider_type: ProviderType,
        credentials: dict[str, Any],
    ) -> dict:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Account:
        ...
