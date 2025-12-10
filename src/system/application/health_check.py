import asyncio
from datetime import datetime, timezone

import asyncpg
from dependency_injector.wiring import inject, Provide

from src.system.domain.repositories import IHealthProbe
from src.system.domain.value_objects.dtos import SystemHealth, ProbeResult
from src.system.domain.value_objects.enums import ProbeType, HealthStatus
from src.shared.domain import IDatabaseContext
from src.shared.infrastructure.logger import LoggerFactory


class HealthCheckService:
    @inject
    def __init__(
        self,
        repository_to_context: dict[IHealthProbe, IDatabaseContext] = Provide['repository_to_context_factory'],
        logger_factory: LoggerFactory = Provide['logger_factory'],
    ) -> None:
        self._logger = logger_factory.get_logger(__name__)
        self._repo2ctx = repository_to_context

    async def probe(
        self,
        probe_type: ProbeType = ProbeType.READINESS,
    ) -> SystemHealth:
        results = []
        if probe_type == ProbeType.READINESS:
            results = await asyncio.gather(
                *[self.__service_probe(repo, ctx) for repo, ctx in self._repo2ctx.items()],
                return_exceptions=True,
            )
        status = HealthStatus.UNHEALTHY
        if all(results):
            status = HealthStatus.HEALTHY
        return SystemHealth(
            status=status,
            probes=results,
            timestamp=datetime.now(tz=timezone.utc),
        )

    async def __service_probe(
        self,
        probe_repository: IHealthProbe,
        service_context_factory: IDatabaseContext,
    ) -> ProbeResult:
        health_status = HealthStatus.HEALTHY
        try:
            async with service_context_factory as ctx:
                await probe_repository.probe(ctx)
        except asyncpg.InterfaceError:
            health_status = HealthStatus.UNHEALTHY
        except Exception as e:
            health_status = HealthStatus.UNHEALTHY
            self._logger.error(e)
        return ProbeResult(
            name=probe_repository.name,
            status=health_status,
        )
