from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependency_injector.wiring import inject, Provide

from src.infrastructure.config import Settings
from src.infrastructure.logger import LoggerFactory


class MiddlewaresManager:
    @inject
    def __init__(
        self,
        app: FastAPI,
        logger_factory: LoggerFactory = Provide['infrastructure.logger_factory'],
        settings: Settings = Provide['infrastructure.settings'],
    ) -> None:
        self._app = app
        self._settings = settings
        self._logger = logger_factory.get_logger(__name__)
        self._middleware_to_kwargs = {
            CORSMiddleware: {
                'allow_origins': self._settings.CORS_ALLOW_ORIGINS,
                'allow_credentials': True,
                'allow_methods': ['*'],
                'allow_headers': ['*'],
            },
        }

    def register_middlewares(self) -> None:
        for middleware, kwargs in self._middleware_to_kwargs.items():
            self._app.add_middleware(middleware, **kwargs)
        self._logger.debug('All middlewares registered')
