from typing import Type
import msgspec

from src.domain.events.base import DomainEvent


class EventRegistry:
    def __init__(self):
        self._events: dict[str, Type[DomainEvent]] = {}
        self._decoders: dict[str, msgspec.json.Decoder] = {}
    
    def register(self, event_class: Type[DomainEvent]) -> None:
        temp_instance = event_class(event_id=None)
        event_type = temp_instance.event_type
        self._events[event_type] = event_class
        self._decoders[event_type] = msgspec.json.Decoder(event_class)
    
    def deserialize(self, event_type: str, payload: bytes) -> DomainEvent:
        decoder = self._decoders.get(event_type)
        if not decoder:
            raise ValueError(f"Unknown event type: {event_type}")
        
        return decoder.decode(payload)
    
    def get_event_types(self) -> list[str]:
        return list(self._events.keys())
