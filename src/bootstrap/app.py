from fastapi import FastAPI

from config import logger
from src.bootstrap.lifespan import LifespanManager
from src.bootstrap.middleware import register_middlewares
from src.bootstrap.exception_handlers import register_exception_handlers
from src.api import router as api_router
from src.well_known import router as well_known_router


def create_app() -> FastAPI:
    lifespan_manager = LifespanManager()
    app = FastAPI(
        title='Auth Service',
        version='1.0.0',
        docs_url='/swagger',
        redoc_url='/redoc',
        lifespan=lifespan_manager.lifespan,
    )
    register_middlewares(app)
    register_exception_handlers(app)
    _include_routers(app)
    logger.info('Application created successfully')
    return app


def _include_routers(app: FastAPI) -> None:
    app.include_router(well_known_router)
    app.include_router(api_router)
    logger.debug('All routers included')
