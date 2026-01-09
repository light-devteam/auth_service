from abc import ABC, abstractmethod
from datetime import datetime

from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain.value_objects import AccessToken, ProviderConfig


class IAccessTokenIssuer(ABC):
    @abstractmethod
    async def issue(
        self,
        issued_at: datetime,
        identity: Identity,
        provider_config: ProviderConfig,
    ) -> AccessToken:
        ...
