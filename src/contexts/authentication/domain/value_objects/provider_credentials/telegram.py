from src.contexts.authentication.domain.value_objects.provider_credentials.base import ProviderCredentials
from src.contexts.authentication.domain.value_objects.id import TelegramAccountID


class TelegramProviderCredentials(ProviderCredentials):
    account_id: int

    def __post_init__(self) -> None:
        TelegramAccountID(self.bot_id)
