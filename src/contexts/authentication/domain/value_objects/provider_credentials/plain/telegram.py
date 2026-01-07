from src.contexts.authentication.domain.value_objects.provider_credentials.plain.base import ProviderPlainCredentials
from src.contexts.authentication.domain.value_objects.id import TelegramAccountID


class TelegramProviderPlainCredentials(ProviderPlainCredentials):
    account_id: TelegramAccountID
