from datetime import datetime

from pydantic import BaseModel, field_serializer

from src.contexts.system.delivery.http.health.schemas import ProbeResult
from src.contexts.system.domain.value_objects import HealthStatus


class SystemHealth(BaseModel):
    status: HealthStatus
    probes: list[ProbeResult]
    timestamp: datetime

    @field_serializer('timestamp', when_used='json')
    def serialize_timestamp_json(self, value: datetime) -> float:
        return value.timestamp()
