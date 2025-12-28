from dependency_injector import containers, providers

from src.infrastructure.logger import LoggerFactory
from src.infrastructure.config import Settings
from src.infrastructure.persistence import (
    PostgresClient,
    RedisClient,
    PostgresUnitOfWork,
    RedisSession,
)

from src.contexts.system.infrastructure import PostgresProbe, RedisProbe
from src.contexts.system.application import HealthCheckService

from src.contexts.jwk.domain.mappers import JWKMapper
from src.contexts.jwk.infrastructure import JWKRepository
from src.contexts.jwk.application import JWKService
from src.contexts.jwk.domain.services import JWKTokenService

from src.domain.mappers import AccountMapper
from src.infrastructure.repositories import AccountRepository

from src.contexts.authentication.domain.mappers import AccountMapper as AccountAuthMapper
from src.contexts.authentication.infrastructure import AccountRepository as AccountAuthRepository
from src.contexts.authentication.application import AccountApplicationService

from src.contexts.authentication.domain.mappers import ProviderMapper as ProviderAuthMapper
from src.contexts.authentication.infrastructure import ProviderRepository as ProviderAuthRepository
from src.contexts.authentication.application import ProviderApplicationService

from src.contexts.authentication.domain.services import IdentityDomainService


class DIContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            'src.bootstrap',
            'src.infrastructure.repositories',
            'src.contexts.system.application',
            'src.contexts.system.delivery',
            'src.contexts.jwk.domain.value_objects',
            'src.contexts.jwk.infrastructure.repositories',
            'src.contexts.jwk.application',
            'src.contexts.jwk.delivery.http',
            'src.contexts.authentication.infrastructure.repositories',
            'src.contexts.authentication.application',
            'src.contexts.authentication.delivery.http',
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

    accounts_mapper = providers.Singleton(AccountMapper)
    accounts_repository = providers.Singleton(AccountRepository)

    accounts_auth_mapper = providers.Singleton(AccountAuthMapper)
    accounts_auth_repository = providers.Singleton(AccountAuthRepository)
    accounts_application_service = providers.Singleton(AccountApplicationService)

    provider_auth_mapper = providers.Singleton(ProviderAuthMapper)
    provider_auth_repository = providers.Singleton(ProviderAuthRepository)
    provider_application_service = providers.Singleton(ProviderApplicationService)

    identity_domain_service = providers.Singleton(IdentityDomainService)