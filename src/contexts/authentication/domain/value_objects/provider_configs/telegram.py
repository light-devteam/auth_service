from src.contexts.authentication.domain.value_objects.provider_configs.base import ProviderConfig


class TelegramProviderConfig(ProviderConfig, forbid_unknown_fields=True):
    data_check_url: str
