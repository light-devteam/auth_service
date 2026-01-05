from typing import Any

import msgspec

from src.contexts.authentication.domain.value_objects import PasswordProviderCredentials
from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.entities import Session
from src.contexts.authentication.domain.providers import IProvider
from src.contexts.authentication.domain.value_objects import PasswordProviderConfig
from src.contexts.authentication.domain.exceptions import ProviderConfigInvalid


class PasswordProvider(IProvider):
    async def authenticate(
        self,
        account_id: AccountID,
        credentials: PasswordProviderCredentials,
    ) -> Session:
        ...

    def validate_config(
        self,
        config: dict[str, Any],
    ) -> PasswordProviderConfig:
        try:
            return msgspec.json.decode(
                msgspec.json.encode(config),
                type=PasswordProviderConfig,
            )
        except (msgspec.ValidationError, TypeError) as e:
            raise ProviderConfigInvalid(f'Password provider invalid config: {e}')

    def validate_credentials(
        self,
        credentials: dict[str, Any],
    ) -> PasswordProviderCredentials:
        try:
            return msgspec.json.decode(
                msgspec.json.encode(credentials),
                type=PasswordProviderCredentials,
            )
        except (msgspec.ValidationError, TypeError) as e:
            raise ProviderConfigInvalid(f'Password provider invalid credentials: {e}')
