from msgspec import Struct

from src.contexts.system.domain.value_objects.enums.health_status import HealthStatus


class ProbeResult(Struct, frozen=True):
    name: str
    status: HealthStatus

    def __bool__(self) -> bool:
        return self.status == HealthStatus.HEALTHY
