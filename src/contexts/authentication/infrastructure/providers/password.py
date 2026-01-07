from typing import Any, Type

import msgspec
import bcrypt

from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.entities import Session
from src.contexts.authentication.domain.providers import IProvider
from src.contexts.authentication.domain.value_objects import (
    PasswordProviderPlainCredentials,
    PasswordProviderSecureCredentials,
    PasswordProviderConfig,
    Login,
    Password,
    HashedPassword,
)
from src.contexts.authentication.domain.exceptions import ProviderConfigInvalid


class PasswordProvider(IProvider):
    def __init__(self) -> None:
        self._credentials_decoder = msgspec.json.Decoder(
            PasswordProviderPlainCredentials,
            dec_hook=self.__decode_credentials_hook,
        )
        self._config_decoder = msgspec.json.Decoder(
            PasswordProviderConfig,
            dec_hook=self.__decode_config_hook,
        )

    async def authenticate(
        self,
        account_id: AccountID,
        credentials: PasswordProviderPlainCredentials,
    ) -> Session:
        ...

    def validate_config(
        self,
        config: dict[str, Any],
    ) -> PasswordProviderConfig:
        try:
            return self._config_decoder.decode(msgspec.json.encode(config))
        except (msgspec.ValidationError, TypeError) as e:
            raise ProviderConfigInvalid(f'Password provider invalid config: {e}')

    def validate_credentials(
        self,
        credentials: dict[str, Any],
    ) -> PasswordProviderPlainCredentials:
        try:
            return self._credentials_decoder.decode(msgspec.json.encode(credentials))
        except (msgspec.ValidationError, TypeError) as e:
            raise ProviderConfigInvalid(f'Password provider invalid credentials: {e}')

    def secure_credentials(
        self,
        credentials: PasswordProviderPlainCredentials,
    ) -> PasswordProviderSecureCredentials:
        return PasswordProviderSecureCredentials(
            login=credentials.login,
            password=HashedPassword(credentials.password),
        )

    def __decode_credentials_hook(self, type_: Type[Any], obj: Any) -> Any:
        if type_ is Login:
            return Login(obj)
        if type_ is Password:
            return Password(obj)
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')

    def __decode_config_hook(self, type_: Type[Any], obj: Any) -> Any:
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')
