from abc import ABC, abstractmethod
from typing import Any

from src.contexts.authentication.domain.value_objects import (
    ProviderConfig,
    ProviderPlainCredentials,
    ProviderSecureCredentials,
)
from src.contexts.authentication.domain import token_managers


class IProvider(ABC):
    @abstractmethod
    async def authenticate(
        self,
        input_credentials: ProviderPlainCredentials,
        identity_credentials: dict[str, Any],
    ) -> None:
        ...

    @abstractmethod
    def validate_config(
        self,
        config: dict[str, Any],
    ) -> ProviderConfig:
        ...

    @abstractmethod
    async def validate_credentials(
        self,
        credentials: dict[str, Any],
        provider_config: ProviderConfig,
    ) -> ProviderPlainCredentials:
        ...

    @abstractmethod
    def secure_credentials(
        self,
        credentials: ProviderPlainCredentials,
    ) -> ProviderSecureCredentials:
        ...

    @abstractmethod
    def get_login_field(self, credentials: ProviderPlainCredentials) -> str:
        ...

    @property
    @abstractmethod
    def access_token_manager(self) -> token_managers.IAccessTokenManager:
        ...

    @property
    @abstractmethod
    def refresh_token_manager(self) -> token_managers.IRefreshTokenManager:
        ...
