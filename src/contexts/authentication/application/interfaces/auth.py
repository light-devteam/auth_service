from abc import ABC, abstractmethod
from typing import Any

from src.contexts.authentication.domain.value_objects import (
    ProviderType,
    AccessToken,
    RefreshToken,
)


class IAuthService(ABC):
    @abstractmethod
    async def get_token(
        self,
        provider_type: ProviderType,
        credentials: dict[str, Any],
    ) -> tuple[AccessToken, RefreshToken]:
        ...
