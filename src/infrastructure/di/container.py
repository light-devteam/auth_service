from dependency_injector import containers, providers

from src.shared.infrastructure.logger import LoggerFactory
from src.shared.infrastructure.config import Settings
from src.infrastructure.persistence import PostgresClient, RedisClient

class DIContainer(containers.DeclarativeContainer):
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
