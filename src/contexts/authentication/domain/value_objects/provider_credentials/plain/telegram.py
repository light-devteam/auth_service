from typing import Optional

from src.contexts.authentication.domain.value_objects.provider_credentials.plain.base import ProviderPlainCredentials
from src.contexts.authentication.domain.value_objects.id import TelegramAccountID


class TelegramProviderPlainCredentials(ProviderPlainCredentials):
    id: TelegramAccountID
    first_name: str
    auth_date: str
    hash: str
    last_name: Optional[str] = ''
    username: Optional[str] = ''
    photo_url: Optional[str] = ''
