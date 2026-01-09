from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from dependency_injector.wiring import inject, Provide

from src.domain.events import IEventBus, EventRegistry, AppStartedEvent, JWKSUpdatedEvent
from src.infrastructure.di import DIContainer
from src.infrastructure.logger import LoggerFactory
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
        logger_factory: LoggerFactory = Provide['infrastructure.logger_factory'],
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
            await self._start_event_bus()
        except Exception as e:
            self._logger.error(f'Failed to start application when connect storages: {e}')
            raise
        self._logger.info('Application started successfully')
        await self.container.infrastructure.event_bus().publish(AppStartedEvent())

    async def _shutdown(self) -> None:
        self._logger.info('Shutting down application...')
        try:
            await self._disconnect_storages()
            await self._stop_event_bus()
        except Exception as e:
            self._logger.error(f'Error during shutdown: {e}')
        self.container.unwire()
        self._logger.info('Application stopped successfully')

    @inject
    async def _connect_storages(
        self,
        postgres_client: PostgresClient = Provide['infrastructure.postgres_client'],
        redis_client: RedisClient = Provide['infrastructure.redis_client'],
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
        postgres_client: PostgresClient = Provide['infrastructure.postgres_client'],
        redis_client: RedisClient = Provide['infrastructure.redis_client'],
    ) -> None:
        self._logger.debug('Disconnecting from PostgreSQL...')
        await postgres_client.disconnect()
        self._logger.info('PostgreSQL disconnected')
        self._logger.debug('Disconnecting from Redis...')
        await redis_client.disconnect()
        self._logger.info('Redis disconnected')

    @inject
    async def _start_event_bus(
        self,
        event_bus: IEventBus = Provide['infrastructure.event_bus'],
        event_registry: EventRegistry = Provide['infrastructure.event_registry'],
    ) -> None:
        self._logger.debug('Registering integration events...')
        self._register_all_events(event_registry)
        self._logger.info('Integration events registered')
        self._logger.debug('Setting up event handlers...')
        await self._setup_all_handlers()
        self._logger.info('Event handlers registered')
        self._logger.debug('Starting event bus...')
        await event_bus.start()
        self._logger.info('Event bus started')

    @inject
    async def _stop_event_bus(
        self,
        event_bus: IEventBus = Provide['infrastructure.event_bus'],
    ) -> None:
        self._logger.debug('Stopping event bus...')
        await event_bus.stop()
        self._logger.info('Event bus stopped')

    def _register_all_events(self, registry: EventRegistry) -> None:
        events = [
            AppStartedEvent,
            JWKSUpdatedEvent,
        ]
        for event in events:
            registry.register(event)

    async def _setup_all_handlers(self) -> None:
        contexts = [
            self.container.auth.context(),
            self.container.jwk.context(),
        ]
        for context in contexts:
            await context.register_handlers()
