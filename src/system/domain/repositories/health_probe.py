from abc import ABC, abstractmethod

from src.shared.domain import IDatabaseContext


class IHealthProbe(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def probe(self, ctx: IDatabaseContext) -> None:
        raise NotImplementedError()
