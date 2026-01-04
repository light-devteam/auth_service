from abc import ABC, abstractmethod
from typing import Any

from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.entities import Session
from src.contexts.authentication.domain.value_objects import ProviderCredentials
from src.contexts.authentication.domain.value_objects import ProviderConfig


class IProvider(ABC):
    @abstractmethod
    async def authenticate(
        self,
        account_id: AccountID,
        credentials: ProviderCredentials,
    ) -> Session:
        ...

    @abstractmethod
    def validate_config(
        self,
        config: dict[str, Any],
    ) -> ProviderConfig:
        ...
