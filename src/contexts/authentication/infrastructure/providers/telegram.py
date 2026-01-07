from typing import Any, Type

import msgspec

from src.contexts.authentication.domain.value_objects import (
    TelegramProviderPlainCredentials,
    TelegramProviderSecureCredentials,
)
from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.entities import Session
from src.contexts.authentication.domain.providers import IProvider
from src.contexts.authentication.domain.value_objects import TelegramProviderConfig, TelegramAccountID
from src.contexts.authentication.domain.exceptions import ProviderConfigInvalid


class TelegramProvider(IProvider):
    def __init__(self) -> None:
        self._credentials_decoder = msgspec.json.Decoder(
            TelegramProviderPlainCredentials,
            dec_hook=self.__decode_credentials_hook,
        )
        self._config_decoder = msgspec.json.Decoder(
            TelegramProviderConfig,
            dec_hook=self.__decode_config_hook,
        )

    async def authenticate(
        self,
        account_id: AccountID,
        credentials: TelegramProviderPlainCredentials,
    ) -> Session:
        ...

    def validate_config(
        self,
        config: dict[str, Any],
    ) -> TelegramProviderConfig:
        try:
            return self._config_decoder.decode(msgspec.json.encode(config))
        except (msgspec.ValidationError, TypeError) as e:
            raise ProviderConfigInvalid(f'Telegram provider invalid config: {e}')

    def validate_credentials(
        self,
        credentials: dict[str, Any],
    ) -> TelegramProviderPlainCredentials:
        try:
            return self._credentials_decoder.decode(msgspec.json.encode(credentials))
        except (msgspec.ValidationError, TypeError) as e:
            raise ProviderConfigInvalid(f'Telegram provider invalid credentials: {e}')

    def secure_credentials(
        self,
        credentials: TelegramProviderPlainCredentials,
    ) -> TelegramProviderSecureCredentials:
        return TelegramProviderSecureCredentials(
            account_id=credentials.account_id,
        )

    def __decode_credentials_hook(self, type_: Type[Any], obj: Any) -> Any:
        if type_ is TelegramAccountID:
            return TelegramAccountID(obj)
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')

    def __decode_config_hook(self, type_: Type[Any], obj: Any) -> Any:
        if type_ is TelegramAccountID:
            return TelegramAccountID(obj)
        raise TypeError(f'Unsupported type {type_} for value {obj!r}')
