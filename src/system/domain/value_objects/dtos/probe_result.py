from msgspec import Struct

from src.system.domain.value_objects.enums import HealthStatus


class ProbeResult(Struct, frozen=True):
    name: str
    status: HealthStatus

    def __bool__(self) -> bool:
        return self.status == HealthStatus.HEALTHY
