from datetime import datetime

from pydantic import BaseModel, field_serializer

from src.system.delivery.http.health.schemas.probe_result import ProbeResult
from src.system.domain.value_objects.enums import HealthStatus


class SystemHealth(BaseModel):
    status: HealthStatus
    probes: list[ProbeResult]
    timestamp: datetime

    @field_serializer('timestamp', when_used='json')
    def serialize_timestamp_json(self, value: datetime) -> float:
        return value.timestamp()
