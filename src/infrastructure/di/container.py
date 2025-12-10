from dependency_injector import containers, providers

from src.shared.infrastructure.logger import LoggerFactory
from src.shared.infrastructure.config import Settings
from src.infrastructure.persistence import (
    PostgresClient,
    RedisClient,
    PostgresUnitOfWork,
    RedisSession,
)
from src.system.infrastructure.repositories import PostgresProbe, RedisProbe
from src.system.application import HealthCheckService


class DIContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            'src.bootstrap',
            'src.system.application',
            'src.system.delivery',
        ],
    )

    settings = providers.Singleton(Settings)
    logger_factory = providers.Singleton(LoggerFactory, settings=settings)

    postgres_client = providers.Singleton(
        PostgresClient,
        db_url=settings.provided.POSTGRES_URL,
    )
    redis_client = providers.Singleton(
        RedisClient,
        db_url=settings.provided.REDIS_URL,
    )

    postgres_uow = providers.Factory(PostgresUnitOfWork, client=postgres_client)
    redis_session = providers.Factory(RedisSession, client=redis_client)

    postgres_probe_repository = providers.Singleton(PostgresProbe)
    redis_probe_repository = providers.Singleton(RedisProbe)

    repository_to_context_factory = providers.Dict({
        postgres_probe_repository(): postgres_uow,
        redis_probe_repository(): redis_session,
    })

    healthcheck_application_service = providers.Singleton(HealthCheckService)
