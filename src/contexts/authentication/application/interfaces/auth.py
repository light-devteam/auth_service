from abc import ABC, abstractmethod
from typing import Any

from src.contexts.authentication.domain.value_objects import ProviderType, Token, AuthContext


class IAuthService(ABC):
    @abstractmethod
    async def get_token(
        self,
        provider_type: ProviderType,
        credentials: dict[str, Any],
    ) -> tuple[Token, Token]:
        ...

    @abstractmethod
    async def refresh(
        self,
        refresh_token: str,
    ) -> tuple[Token, Token]:
        ...

    @abstractmethod
    async def introspect(
        self,
        access_token: str,
    ) -> AuthContext:
        ...
