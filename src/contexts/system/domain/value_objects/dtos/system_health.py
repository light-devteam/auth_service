from datetime import datetime

from msgspec import Struct

from src.contexts.system.domain.value_objects.dtos.probe_result import ProbeResult
from src.contexts.system.domain.value_objects.enums.health_status import HealthStatus


class SystemHealth(Struct, frozen=True):
    status: HealthStatus
    probes: list[ProbeResult]
    timestamp: datetime
