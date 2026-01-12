from typing import Any, Type

import msgspec
from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain import (
    exceptions,
    providers,
    value_objects,
    token_managers,
)


class TelegramProvider(providers.IProvider):
    @inject
    def __init__(
        self,
        access_token_manager: token_managers.IAccessTokenManager = Provide['auth.access_token_jwt_manager'],
        refresh_token_manager: token_managers.IRefreshTokenManager = Provide['auth.refresh_token_b64_manager'],
    ) -> None:
        self._credentials_decoder = msgspec.json.Decoder(
            value_objects.TelegramProviderPlainCredentials,
            dec_hook=self.__decode_credentials_hook,
        )
        self._config_decoder = msgspec.json.Decoder(
            value_objects.TelegramProviderConfig,
            dec_hook=self.__decode_config_hook,
        )
        self._access_token_manager = access_token_manager
        self._refresh_token_manager = refresh_token_manager

    async def authenticate(
        self,
        input_credentials: value_objects.TelegramProviderPlainCredentials,
        identity_credentials: dict[str, Any],
    ) -> None:
        # TODO: logic
        raise exceptions.InvalidCredentials()

    def validate_config(
        self,
        config: dict[str, Any],
    ) -> value_objects.TelegramProviderConfig:
        try:
            return self._config_decoder.decode(msgspec.json.encode(config))
        except (msgspec.ValidationError, TypeError) as e:
            raise exceptions.ProviderConfigInvalid(f'Telegram provider invalid config: {e}')

    def validate_credentials(
        self,
        credentials: dict[str, Any],
    ) -> value_objects.TelegramProviderPlainCredentials:
        try:
            return self._credentials_decoder.decode(msgspec.json.encode(credentials))
        except (msgspec.ValidationError, TypeError) as e:
            raise exceptions.InvalidCredentials(f'Telegram provider invalid credentials: {e}')

    def secure_credentials(
        self,
        credentials: value_objects.TelegramProviderPlainCredentials,
    ) -> value_objects.TelegramProviderSecureCredentials:
        return value_objects.TelegramProviderSecureCredentials(
            login=credentials.account_id,
        )

    def get_login_field(self, credentials: value_objects.TelegramProviderPlainCredentials) -> str:
        return credentials.account_id

    @property
    def access_token_manager(self) -> token_managers.IAccessTokenManager:
        return self._access_token_manager

    @property
    def refresh_token_manager(self) -> token_managers.IRefreshTokenManager:
        return self._refresh_token_manager

    def __decode_credentials_hook(self, type_: Type[Any], obj: Any) -> Any:
        if type_ is value_objects.TelegramAccountID:
            return value_objects.TelegramAccountID(obj)
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')

    def __decode_config_hook(self, type_: Type[Any], obj: Any) -> Any:
        if type_ is value_objects.TelegramAccountID:
            return value_objects.TelegramAccountID(obj)
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')
