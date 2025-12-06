from dependency_injector import containers, providers

from src.shared.infrastructure.logger import LoggerFactory
from src.shared.infrastructure.config import Settings

class DIContainer(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    logger_factory = providers.Singleton(LoggerFactory, settings=settings)
