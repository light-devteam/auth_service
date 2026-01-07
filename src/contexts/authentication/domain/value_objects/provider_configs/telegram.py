from src.contexts.authentication.domain.value_objects.provider_configs.base import ProviderConfig
from src.contexts.authentication.domain.value_objects.id import TelegramAccountID


class TelegramProviderConfig(ProviderConfig, forbid_unknown_fields=True):
    bot_id: TelegramAccountID
