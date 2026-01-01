from fastapi import Depends, Response, status
from dependency_injector.wiring import inject, Provide
from msgspec import json

from src.contexts.system.delivery.http.health.router import router
from src.contexts.system.delivery.http.health.schemas import SystemHealth
from src.contexts.system.application import IHealthCheckService
from src.contexts.system.domain.value_objects import ProbeType, HealthStatus


@router.get('/ready')
@inject
async def check_readiness(
    response: Response,
    healthcheck_service: IHealthCheckService = Depends(
        Provide['system.healthcheck_service'],
    ),
) -> SystemHealth:
    system_health = await healthcheck_service.probe(ProbeType.READINESS)
    if system_health.status == HealthStatus.UNHEALTHY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return SystemHealth.model_validate_json(json.encode(system_health))
