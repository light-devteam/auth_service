from typing import Any

import msgspec

from src.contexts.authentication.domain.value_objects import TelegramProviderCredentials
from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.entities import Session
from src.contexts.authentication.domain.providers import IProvider
from src.contexts.authentication.domain.value_objects import TelegramProviderConfig
from src.contexts.authentication.domain.exceptions import ProviderConfigInvalid


class TelegramProvider(IProvider):
    async def authenticate(
        self,
        account_id: AccountID,
        credentials: TelegramProviderCredentials,
    ) -> Session:
        ...

    def validate_config(
        self,
        config: dict[str, Any],
    ) -> TelegramProviderConfig:
        try:
            return msgspec.json.decode(
                msgspec.json.encode(config),
                type=TelegramProviderConfig,
            )
        except (msgspec.ValidationError, TypeError) as e:
            raise ProviderConfigInvalid(f'Telegram provider invalid config: {e}')
