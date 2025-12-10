from fastapi import Depends, Response, status
from dependency_injector.wiring import inject, Provide
from msgspec import json

from src.system.delivery.http.health.router import router
from src.system.delivery.http.health.schemas import SystemHealth
from src.system.application import HealthCheckService
from src.system.domain.value_objects.enums import ProbeType, HealthStatus


@router.get('/live')
@inject
async def check_liveness(
    response: Response,
    healthcheck_service: HealthCheckService = Depends(
        Provide['healthcheck_application_service'],
    ),
) -> None:
    system_health = await healthcheck_service.probe(ProbeType.LIVENESS)
    if system_health.status == HealthStatus.UNHEALTHY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return SystemHealth.model_validate_json(json.encode(system_health))
