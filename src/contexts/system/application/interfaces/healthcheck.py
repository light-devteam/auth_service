from abc import ABC, abstractmethod

from src.contexts.system.domain.value_objects import ProbeType, SystemHealth


class IHealthCheckService(ABC):
    @abstractmethod
    async def probe(
        self,
        probe_type: ProbeType = ProbeType.READINESS,
    ) -> SystemHealth:
        ...
