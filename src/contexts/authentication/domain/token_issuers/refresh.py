from abc import ABC, abstractmethod
from datetime import datetime

from src.contexts.authentication.domain.value_objects import RefreshToken
from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain.value_objects import ProviderConfig


class IRefreshTokenIssuer(ABC):
    @abstractmethod
    async def issue(
        self,
        issued_at: datetime,
        identity: Identity,
        provider_config: ProviderConfig,
    ) -> RefreshToken:
        ...
