from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from dependency_injector.wiring import inject, Provide

from src.infrastructure.di import DIContainer
from src.shared.infrastructure.logger import LoggerFactory


class LifespanManager:
    def __init__(self) -> None:
        self.container = DIContainer()
        self.container.wire(modules=[
            __name__,
            'src.bootstrap.exception_handler',
            'src.bootstrap.app',
        ])

    @asynccontextmanager
    @inject
    async def lifespan(
        self,
        app: FastAPI,
        logger_factory: LoggerFactory = Provide['logger_factory'],
    ) -> AsyncGenerator[None, None]:
        logger = logger_factory.get_logger(__name__)
        logger.info('Starting application...')
#         try:
#             await self._connect_storages()
#         except Exception as e:
#             logger.error(f'Failed to start application when connect storages: {e}')
#             raise
#         try:
#             await self._initialize_jwk()
#         except Exception as e:
#             logger.error(f'Failed to start application when initialize jwk: {e}')
#             raise
        logger.info('Application started successfully')
        yield
        logger.info('Shutting down application...')
#         try:
#             await self._disconnect_storages()
#         except Exception as e:
#             logger.error(f'Error during shutdown: {e}')
#        await self.container.shutdown_resources()
        self.container.unwire()
        logger.info('Application stopped successfully')

#     async def _connect_storages(self) -> None:
#         logger.debug('Connecting to PostgreSQL...')
#         await postgres.connect()
#         logger.info('PostgreSQL connected')
#         logger.debug('Connecting to Redis...')
#         await redis.connect()
#         logger.info('Redis connected')
    
#     async def _disconnect_storages(self) -> None:
#         logger.debug('Disconnecting from PostgreSQL...')
#         await postgres.disconnect()
#         logger.info('PostgreSQL disconnected')
#         logger.debug('Disconnecting from Redis...')
#         await redis.disconnect()
#         logger.info('Redis disconnected')
