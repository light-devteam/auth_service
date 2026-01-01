from abc import ABC, abstractmethod
from typing import Any

from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain.value_objects import ProviderID, IdentityID
from src.domain.value_objects import AccountID


class IIdentityService(ABC):
    @abstractmethod
    async def create(
        self,
        account_id: AccountID,
        provider_id: ProviderID,
        provider_data: dict[str, Any],
    ) -> Identity:
        ...

    @abstractmethod
    async def get_by_id(self, id: IdentityID) -> Identity:
        ...

    @abstractmethod
    async def get_by_account_id(
        self,
        id: AccountID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[Identity]:
        ...

    @abstractmethod
    async def get_by_account_id_and_provider_id(
        self,
        account_id: AccountID,
        provider_id: ProviderID,
    ) -> Identity:
        ...
