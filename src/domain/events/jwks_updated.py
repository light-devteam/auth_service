from typing import Any

from src.domain.events.base import DomainEvent


class JWKSUpdatedEvent(DomainEvent):
    jwks: list[dict] = []

    @property
    def event_type(self) -> str:
        return 'jwks.updated'
