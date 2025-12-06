from fastapi import FastAPI
from dependency_injector.wiring import inject, Provide

from src.bootstrap.lifespan import LifespanManager
# from src.bootstrap.middleware import register_middlewares
from src.bootstrap.exception_handler import ExceptionHandler
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
        # register_middlewares(app)
        ExceptionHandler(self.__app)
        self.__include_routers()
        self.__logger.info('Application created successfully')
        return self.__app

    def __include_routers(self) -> None:
        for router in self._routers:
            self.__app.include_router(router)
        self.__logger.debug(f'Included {len(self._routers)} routers')
