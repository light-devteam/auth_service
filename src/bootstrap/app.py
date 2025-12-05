from fastapi import FastAPI

from src.bootstrap.lifespan import LifespanManager
# from src.bootstrap.middleware import register_middlewares
# from src.bootstrap.exception_handlers import register_exception_handlers


def create_app() -> FastAPI:
    lifespan_manager = LifespanManager()
    app = FastAPI(
        title='Auth Service',
        version='1.0.0',
        docs_url='/swagger',
        redoc_url='/redoc',
        lifespan=lifespan_manager.lifespan,
    )
    # register_middlewares(app)
    # register_exception_handlers(app)
    _include_routers(app)
    # logger.info('Application created successfully')
    return app


def _include_routers(app: FastAPI) -> None:
    # app.include_router(well_known_router)
    # app.include_router(api_router)
    # logger.debug('All routers included')
    ...
