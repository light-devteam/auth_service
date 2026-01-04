from dependency_injector import containers, providers

from src.contexts.authentication.infrastructure.providers import (
    ProviderRegistry,
    PasswordProvider,
    TelegramProvider,
)
from src.contexts.authentication.domain.value_objects import ProviderType


class ProvidersContainer(containers.DeclarativeContainer):
    password = providers.Factory(PasswordProvider)
    telegram = providers.Factory(TelegramProvider)

    registry = providers.Factory(
        ProviderRegistry,
        providers={
            ProviderType.PASSWORD: password,
            ProviderType.TELEGRAM: telegram,
        }
    )
