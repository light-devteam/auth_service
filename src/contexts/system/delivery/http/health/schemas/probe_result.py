from pydantic import BaseModel

from src.contexts.system.domain.value_objects import HealthStatus


class ProbeResult(BaseModel):
    name: str
    status: HealthStatus

