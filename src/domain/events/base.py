from uuid import UUID, uuid4

from msgspec import Struct, field

class DomainEvent(Struct):
    event_id: UUID = field(default_factory=uuid4)

    @property
    def event_type(self) -> str:
        return 'base'
