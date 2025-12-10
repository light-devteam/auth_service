from pydantic import BaseModel

from src.system.domain.value_objects.enums import HealthStatus


class ProbeResult(BaseModel):
    name: str
    status: HealthStatus

