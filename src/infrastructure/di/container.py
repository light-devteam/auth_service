from dependency_injector import containers, providers

from src.infrastructure.logger import LoggerFactory
from src.infrastructure.config import Settings
from src.infrastructure.persistence import (
    PostgresClient,
    RedisClient,
    PostgresUnitOfWork,
    RedisSession,
)
from src.system.infrastructure.repositories import PostgresProbe, RedisProbe
from src.system.application import HealthCheckService

from src.jwk.domain.mappers import JWKMapper
from src.jwk.infrastructure.repositories import JWKRepository
from src.jwk.application import JWKService
from src.jwk.domain.services import JWKTokenService


class DIContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            'src.bootstrap',
            'src.system.application',
            'src.system.delivery',
            'src.jwk.domain.value_objects',
            'src.jwk.infrastructure.repositories',
            'src.jwk.application',
            'src.jwk.delivery.http',
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

    jwk_mapper = providers.Singleton(JWKMapper)

    postgres_probe_repository = providers.Singleton(PostgresProbe)
    redis_probe_repository = providers.Singleton(RedisProbe)
    jwk_repository = providers.Singleton(JWKRepository)

    repository_to_context_factory = providers.Dict({
        postgres_probe_repository(): postgres_uow,
        redis_probe_repository(): redis_session,
    })

    jwk_domain_service = providers.Singleton(JWKTokenService)

    healthcheck_application_service = providers.Singleton(HealthCheckService)
    jwk_application_service = providers.Singleton(JWKService)