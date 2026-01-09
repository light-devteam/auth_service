from typing import Protocol

from src.domain.events.interfaces.bus import IEventBus


class IEventBootstrap(Protocol):
    async def register_handlers(self, event_bus: IEventBus) -> None:
        ...
