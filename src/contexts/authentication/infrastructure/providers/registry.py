from dependency_injector import providers

from src.contexts.authentication.domain.providers import IProviderFactory, IProvider
from src.contexts.authentication.domain.value_objects import ProviderType


class ProviderRegistry(IProviderFactory):
    def __init__(self, providers: dict[str, providers.Factory]):
        self._providers = providers
    
    def get(self, t: ProviderType) -> IProvider:
        factory = self._providers.get(t.value)
        if not factory:
            raise ValueError(f'No provider for {t}')
        return factory()
