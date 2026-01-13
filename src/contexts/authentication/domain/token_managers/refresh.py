from abc import ABC, abstractmethod
from datetime import datetime

from src.contexts.authentication.domain.value_objects import OpaqueToken
from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain.value_objects import ProviderConfig


class IRefreshTokenManager(ABC):
    @abstractmethod
    async def issue(
        self,
        issued_at: datetime,
        identity: Identity,
        provider_config: ProviderConfig,
    ) -> OpaqueToken:
        ...

    @abstractmethod
    async def validate(
        self,
        token: str,
        token_hash: bytes,
    ) -> None:
        ...
