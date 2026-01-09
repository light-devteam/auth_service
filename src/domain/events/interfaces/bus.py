from abc import ABC, abstractmethod

from src.domain.events.base import DomainEvent
from src.domain.events.interfaces.handler import EventHandler


class IEventBus(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        ...

    @abstractmethod
    async def subscribe(
        self,
        event_type: str,
        handler: EventHandler
    ) -> None:
        ...

    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def stop(self) -> None:
        ...
