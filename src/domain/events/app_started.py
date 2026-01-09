from src.domain.events.base import DomainEvent


class AppStartedEvent(DomainEvent):
    @property
    def event_type(self) -> str:
        return 'app.started'
