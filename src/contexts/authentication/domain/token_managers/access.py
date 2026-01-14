from abc import ABC, abstractmethod
from datetime import datetime

from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain.value_objects import Token, ProviderConfig, AuthContext, SessionID


class IAccessTokenManager(ABC):
    @abstractmethod
    async def issue(
        self,
        issued_at: datetime,
        identity: Identity,
        provider_config: ProviderConfig,
        session_id: SessionID,
    ) -> Token:
        ...

    @abstractmethod
    async def validate(
        self,
        token: str,
    ) -> AuthContext:
        ...
