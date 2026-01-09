from dependency_injector.wiring import inject, Provide

from src.domain.events import IEventBus, JWKSUpdatedEvent, AppStartedEvent
from src.contexts.jwk.application import IJWKService
from src.contexts.jwk.domain.mappers import JWKMapper


class JWKContext:
    @inject
    def __init__(
        self,
        jwk_service: IJWKService,
        event_bus: IEventBus = Provide['infrastructure.event_bus'],
        jwk_mapper: JWKMapper = Provide['jwk.mapper']
    ) -> None:
        self._jwk_service = jwk_service
        self._event_bus = event_bus
        self._jwk_mapper = jwk_mapper
        self._cache = {}

    async def register_handlers(self) -> None:
        await self._event_bus.subscribe('app.started', self._handle_app_started)

    async def _handle_app_started(self, event: AppStartedEvent) -> None:
        page = 1
        jwks = []
        while page:
            all_jwk = await self._jwk_service.get_all(page=page, only_active=True)
            if not all_jwk:
                page = 0
            else:
                for jwk in all_jwk:
                    jwks.append(self._jwk_mapper.from_entity(jwk))
                page += 1
        await self._event_bus.publish(JWKSUpdatedEvent(jwks=jwks))
