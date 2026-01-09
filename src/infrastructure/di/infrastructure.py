from dependency_injector import containers, providers

from src.domain.events import EventRegistry, IEventBus
from src.infrastructure.logger import LoggerFactory
from src.infrastructure.config import Settings
from src.infrastructure.persistence import (
    PostgresClient,
    RedisClient,
    PostgresUnitOfWork,
    RedisSession,
    RedisEventBus,
)


class InfrastructureContainer(containers.DeclarativeContainer):
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

    event_registry = providers.Singleton(EventRegistry)

    event_bus = providers.Singleton(
        RedisEventBus,
        redis_client=redis_client,
        event_registry=event_registry,
        logger_factory=logger_factory,
        channel_prefix="events",
    )
