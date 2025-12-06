from fastapi import FastAPI

from src.bootstrap.lifespan import LifespanManager
# from src.bootstrap.middleware import register_middlewares
# from src.bootstrap.exception_handlers import register_exception_handlers

class App:
    def __init__(self) -> None:
        self.lifespan_manager = LifespanManager()
        self.__app = None
        self.__logger = None

    def create(self) -> FastAPI:
        self.__app = FastAPI(
            title='Auth Service',
            version='1.0.0',
            docs_url='/swagger',
            redoc_url='/redoc',
            lifespan=self.lifespan_manager.lifespan,
        )
        self.__logger = self.lifespan_manager.container.logger_factory().get_logger(__name__)
        # register_middlewares(app)
        # register_exception_handlers(app)
        self.__include_routers()
        self.__logger.info('Application created successfully')
        return self.__app

    def __include_routers(self) -> None:
        # app.include_router(well_known_router)
        # app.include_router(api_router)
        self.__logger.debug('All routers included')
        ...
