from abc import ABC, abstractmethod

from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.entities import Session
from src.contexts.authentication.domain.value_objects import ProviderCredentials


class IProvider(ABC):
    @abstractmethod
    async def authenticate(
        self,
        account_id: AccountID,
        credentials: ProviderCredentials,
    ) -> Session:
        ...
