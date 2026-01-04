from src.contexts.authentication.infrastructure.providers.registry import ProviderRegistry
from src.contexts.authentication.infrastructure.providers.password import PasswordProvider
from src.contexts.authentication.infrastructure.providers.telegram import TelegramProvider


__all__ = [
    'ProviderRegistry',
    'PasswordProvider',
    'TelegramProvider',
]
