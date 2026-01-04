from abc import ABC, abstractmethod

from src.contexts.authentication.domain.value_objects import ProviderType
from src.contexts.authentication.domain.providers.provider import IProvider


class IProviderFactory(ABC):
    @abstractmethod
    def get(self, provider_type: ProviderType) -> IProvider:
        ...
