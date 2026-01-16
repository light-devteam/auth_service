from typing import Any, Type

import msgspec
from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain import (
    exceptions,
    providers,
    value_objects,
    token_managers,
)

class PasswordProvider(providers.IProvider):
    @inject
    def __init__(
        self,
        access_token_manager: token_managers.IAccessTokenManager = Provide['auth.access_token_jwt_manager'],
        refresh_token_manager: token_managers.IRefreshTokenManager = Provide['auth.refresh_token_b64_manager'],
    ) -> None:
        self._credentials_decoder = msgspec.json.Decoder(
            value_objects.PasswordProviderPlainCredentials,
            dec_hook=self.__decode_credentials_hook,
        )
        self._config_decoder = msgspec.json.Decoder(
            value_objects.PasswordProviderConfig,
            dec_hook=self.__decode_config_hook,
        )
        self._access_token_manager = access_token_manager
        self._refresh_token_manager = refresh_token_manager

    async def authenticate(
        self,
        input_credentials: value_objects.PasswordProviderPlainCredentials,
        identity_credentials: dict[str, Any],
    ) -> None:
        password_hash = value_objects.HashedPassword.load(identity_credentials['password'])
        if not password_hash.check(input_credentials.password):
            raise exceptions.InvalidCredentials()

    def validate_config(
        self,
        config: dict[str, Any],
    ) -> value_objects.PasswordProviderConfig:
        try:
            return self._config_decoder.decode(msgspec.json.encode(config))
        except (msgspec.ValidationError, TypeError) as e:
            raise exceptions.ProviderConfigInvalid(f'Password provider invalid config: {e}')

    async def validate_credentials(
        self,
        credentials: dict[str, Any],
        provider_config: value_objects.PasswordProviderConfig,
    ) -> value_objects.PasswordProviderPlainCredentials:
        try:
            return self._credentials_decoder.decode(msgspec.json.encode(credentials))
        except (msgspec.ValidationError, TypeError) as e:
            raise exceptions.InvalidCredentials(f'Password provider invalid credentials: {e}')

    def secure_credentials(
        self,
        credentials: value_objects.PasswordProviderPlainCredentials,
    ) -> value_objects.PasswordProviderSecureCredentials:
        return value_objects.PasswordProviderSecureCredentials(
            login=credentials.login,
            password=value_objects.HashedPassword(credentials.password),
        )

    def get_login_field(self, credentials: value_objects.PasswordProviderPlainCredentials) -> str:
        return credentials.login

    @property
    def access_token_manager(self) -> token_managers.IAccessTokenManager:
        return self._access_token_manager

    @property
    def refresh_token_manager(self) -> token_managers.IRefreshTokenManager:
        return self._refresh_token_manager

    def __decode_credentials_hook(self, type_: Type[Any], obj: Any) -> Any:
        if type_ is value_objects.Login:
            return value_objects.Login(obj)
        if type_ is value_objects.Password:
            return value_objects.Password(obj)
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')

    def __decode_config_hook(self, type_: Type[Any], obj: Any) -> Any:
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')
