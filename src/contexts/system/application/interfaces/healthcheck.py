from abc import ABC, abstractmethod
from typing import Literal

from src.contexts.system.domain.value_objects import SystemHealth


class IHealthCheckService(ABC):
    @abstractmethod
    async def probe(
        self,
        probe_type: Literal['Liveness', 'Readiness'] = 'Readiness',
    ) -> SystemHealth:
        ...
