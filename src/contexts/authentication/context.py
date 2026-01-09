from dependency_injector.wiring import inject, Provide

from src.domain.events import IEventBus, JWKSUpdatedEvent


class AuthenticationContext:
    @inject
    def __init__(
        self,
        event_bus: IEventBus = Provide['infrastructure.event_bus']
    ) -> None:
        self._event_bus = event_bus
        self._cache = {}

    async def register_handlers(self) -> None:
        await self._event_bus.subscribe('jwks.updated', self._handle_jwks_updated)

    async def _handle_jwks_updated(self, event: JWKSUpdatedEvent) -> None:
        self._cache['jwks'] = event.jwks

    @property
    def cache(self) -> dict:
        return self._cache
