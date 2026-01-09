from typing import Any, Type

import msgspec

from src.contexts.authentication.domain import (
    exceptions,
    providers,
    value_objects,
)


class TelegramProvider(providers.IProvider):
    def __init__(self) -> None:
        self._credentials_decoder = msgspec.json.Decoder(
            value_objects.TelegramProviderPlainCredentials,
            dec_hook=self.__decode_credentials_hook,
        )
        self._config_decoder = msgspec.json.Decoder(
            value_objects.TelegramProviderConfig,
            dec_hook=self.__decode_config_hook,
        )

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

    def __decode_credentials_hook(self, type_: Type[Any], obj: Any) -> Any:
        if type_ is value_objects.TelegramAccountID:
            return value_objects.TelegramAccountID(obj)
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')

    def __decode_config_hook(self, type_: Type[Any], obj: Any) -> Any:
        if type_ is value_objects.TelegramAccountID:
            return value_objects.TelegramAccountID(obj)
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')
