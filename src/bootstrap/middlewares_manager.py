from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependency_injector.wiring import inject, Provide

from src.shared.infrastructure.config import Settings
from src.shared.infrastructure.logger import LoggerFactory


class MiddlewaresManager:
    @inject
    def __init__(
        self,
        app: FastAPI,
        logger_factory: LoggerFactory = Provide['logger_factory'],
        settings: Settings = Provide['settings'],
    ) -> None:
        self.__app = app
        self.__settings = settings
        self.__logger = logger_factory.get_logger(__name__)
        self.__middleware_to_kwargs = {
            CORSMiddleware: {
                'allow_origins': self.__settings.CORS_ALLOW_ORIGINS,
                'allow_credentials': True,
                'allow_methods': ['*'],
                'allow_headers': ['*'],
            },
        }

    def register_middlewares(self) -> None:
        for middleware, kwargs in self.__middleware_to_kwargs.items():
            self.__app.add_middleware(middleware, **kwargs)
        self.__logger.debug('All middlewares registered')
