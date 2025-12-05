from dependency_injector import containers, providers

from src.infrastructure.logger import LoggerFactory
from config import Settings

class DIContainer(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    logger = providers.Singleton(LoggerFactory, settings=settings)
