from typing import TypedDict

from dependency_injector.wiring import inject, Provide
import jwt

from src.domain.events import IEventBus, JWKSUpdatedEvent


class ContextCache(TypedDict):
    public_jwks: jwt.PyJWKSet
    private_jwks: jwt.PyJWKSet


class AuthenticationContext:
    @inject
    def __init__(
        self,
        event_bus: IEventBus = Provide['infrastructure.event_bus']
    ) -> None:
        self._event_bus = event_bus
        self._cache: ContextCache = {}

    async def register_handlers(self) -> None:
        await self._event_bus.subscribe('jwks.updated', self._handle_jwks_updated)

    async def _handle_jwks_updated(self, event: JWKSUpdatedEvent) -> None:
        public_jwks = []
        private_jwks = []
        for jwk in event.jwks:
            public_jwks.append(jwk['public'])
            private_jwks.append(jwk['private'])
        self._cache['public_jwks'] = jwt.PyJWKSet(public_jwks)
        self._cache['private_jwks'] = jwt.PyJWKSet(private_jwks)

    @property
    def cache(self) -> ContextCache:
        return self._cache
