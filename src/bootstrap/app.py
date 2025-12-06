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
        self.__app = FastAPI(
            title='Auth Service',
            version='1.0.0',
            docs_url='/swagger',
            redoc_url='/redoc',
            lifespan=self.lifespan_manager.lifespan,
        )
        self.__logger = logger_factory.get_logger(__name__)
        middlewares_manager = MiddlewaresManager(self.__app)
        middlewares_manager.register_middlewares()
        exception_handlers_manager = ExceptionHandlersManager(self.__app)
        exception_handlers_manager.register_exception_handlers()
        self.__include_routers()
        self.__logger.info('Application created successfully')
        return self.__app

    def __include_routers(self) -> None:
        for router in self._routers:
            self.__app.include_router(router)
        self.__logger.debug(f'Included {len(self._routers)} routers')
