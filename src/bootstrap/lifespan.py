from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from dependency_injector.wiring import inject, Provide

from src.infrastructure.di import DIContainer
from src.shared.infrastructure.logger import LoggerFactory
from src.infrastructure.persistence import PostgresClient, RedisClient


class LifespanManager:
    def __init__(self) -> None:
        self.container = DIContainer()
        self._logger = None

    @asynccontextmanager
    @inject
    async def lifespan(
        self,
        app: FastAPI,
        logger_factory: LoggerFactory = Provide['logger_factory'],
    ) -> AsyncGenerator[None, None]:
        self._logger = logger_factory.get_logger(__name__)
        try:
            await self._startup()
            yield
        finally:
            await self._shutdown()

    async def _startup(self) -> None:
        self._logger.info('Starting application...')
        try:
            await self._connect_storages()
        except Exception as e:
            self._logger.error(f'Failed to start application when connect storages: {e}')
            raise
        self._logger.info('Application started successfully')

    async def _shutdown(self) -> None:
        self._logger.info('Shutting down application...')
        try:
            await self._disconnect_storages()
        except Exception as e:
            self._logger.error(f'Error during shutdown: {e}')
        self.container.unwire()
        self._logger.info('Application stopped successfully')

    @inject
    async def _connect_storages(
        self,
        postgres_client: PostgresClient = Provide['postgres_client'],
        redis_client: RedisClient = Provide['redis_client'],
    ) -> None:
        self._logger.debug('Connecting to PostgreSQL...')
        await postgres_client.connect()
        self._logger.info('PostgreSQL connected')
        self._logger.debug('Connecting to Redis...')
        await redis_client.connect()
        self._logger.info('Redis connected')

    @inject
    async def _disconnect_storages(
        self,
        postgres_client: PostgresClient = Provide['postgres_client'],
        redis_client: RedisClient = Provide['redis_client'],
    ) -> None:
        self._logger.debug('Disconnecting from PostgreSQL...')
        await postgres_client.disconnect()
        self._logger.info('PostgreSQL disconnected')
        self._logger.debug('Disconnecting from Redis...')
        await redis_client.disconnect()
        self._logger.info('Redis disconnected')
