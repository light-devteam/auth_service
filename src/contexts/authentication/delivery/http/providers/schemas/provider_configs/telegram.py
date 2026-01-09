from src.contexts.authentication.delivery.http.providers.schemas.provider_configs.base import BaseProviderConfig


class TelegramProviderConfig(BaseProviderConfig):
    bot_id: int
