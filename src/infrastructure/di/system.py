from dependency_injector import containers, providers

from src.contexts.system.infrastructure import PostgresProbe, RedisProbe
from src.contexts.system.application.services import HealthCheckApplicationService
from src.infrastructure.di.infrastructure import InfrastructureContainer

class SystemContainer(containers.DeclarativeContainer):
    def __init__(self, infrastructure: InfrastructureContainer) -> None:
        self.infrastructure = infrastructure
        super().__init__()

    postgres_uow = providers.Factory()
    redis_session = providers.Factory()

    postgres_probe_repository = providers.Singleton(PostgresProbe)
    redis_probe_repository = providers.Singleton(RedisProbe)

    repository_to_context_factory = providers.Dict({
        postgres_probe_repository(): postgres_uow,
        redis_probe_repository(): redis_session,
    })

    healthcheck_service = providers.Singleton(HealthCheckApplicationService)
