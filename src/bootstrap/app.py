from fastapi import FastAPI
from dependency_injector.wiring import inject, Provide

from src.bootstrap.lifespan import LifespanManager
from src.bootstrap.middlewares_manager import MiddlewaresManager
from src.bootstrap.exception_handlers_manager import ExceptionHandlersManager
from src.shared.infrastructure.logger import LoggerFactory

class App:
    def __init__(self) -> None:
        self.lifespan_manager = LifespanManager()
        self.__app = None
        self.__logger = None
        self._routers = []

    @inject
    def create(
        self,
        logger_factory: LoggerFactory = Provide['logger_factory'],
    ) -> FastAPI:
        self._app = FastAPI(
            title='Auth Service',
            version='1.0.0',
            docs_url='/swagger',
            redoc_url='/redoc',
            lifespan=self.lifespan_manager.lifespan,
        )
        self._logger = logger_factory.get_logger(__name__)
        middlewares_manager = MiddlewaresManager(self._app)
        middlewares_manager.register_middlewares()
        exception_handlers_manager = ExceptionHandlersManager(self._app)
        exception_handlers_manager.register_exception_handlers()
        self.__include_routers()
        self._logger.info('Application created successfully')
        return self._app

    def __include_routers(self) -> None:
        for router in self._routers:
            self._app.include_router(router)
        self._logger.debug(f'Included {len(self._routers)} routers')
