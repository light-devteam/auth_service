from src.contexts.authentication.delivery.http.providers.schemas.provider_configs.base import BaseProviderConfig


class TelegramProviderConfig(BaseProviderConfig):
    data_check_url: str
