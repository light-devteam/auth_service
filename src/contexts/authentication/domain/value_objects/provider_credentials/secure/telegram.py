from src.contexts.authentication.domain.value_objects.provider_credentials.secure.base import ProviderSecureCredentials
from src.contexts.authentication.domain.value_objects.id import TelegramAccountID


class TelegramProviderSecureCredentials(ProviderSecureCredentials):
    account_id: TelegramAccountID
