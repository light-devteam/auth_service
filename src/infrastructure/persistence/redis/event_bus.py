import asyncio
from typing import Dict, List
import msgspec

from src.domain.events import DomainEvent, EventHandler, IEventBus
from src.domain.events.registry import EventRegistry
from src.infrastructure.logger import LoggerFactory
from src.infrastructure.persistence.redis.client import RedisClient


class RedisEventBus(IEventBus):
    def __init__(
        self,
        redis_client: RedisClient,
        event_registry: EventRegistry,
        logger_factory: LoggerFactory,
        channel_prefix: str = 'events'
    ):
        self._redis_client = redis_client
        self._registry = event_registry
        self._channel_prefix = channel_prefix
        self._logger = logger_factory.get_logger(__name__)
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._pubsub = None
        self._listen_task = None
        self._encoder = msgspec.json.Encoder()
    
    async def publish(self, event: DomainEvent) -> None:
        channel = f"{self._channel_prefix}:{event.event_type}"
        try:
            payload = self._encoder.encode(event)
            await self._redis_client.connection.publish(channel, payload)
            self._logger.debug(
                f'Published event {event.event_type} to {channel}',
                extra={'event_id': str(event.event_id)}
            )
        except Exception as e:
            self._logger.error(
                f'Failed to publish event {event.event_type}: {e}',
                exc_info=True
            )
            raise

    async def subscribe(self, event_type: str, handler: EventHandler) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        self._logger.info(f'Subscribed handler to event type: {event_type}')

    async def start(self) -> None:
        if self._listen_task is not None:
            self._logger.warning('Event bus already started')
            return
        self._pubsub = self._redis_client.connection.pubsub()
        channels = [
            f'{self._channel_prefix}:{event_type}'
            for event_type in self._handlers.keys()
        ]
        if not channels:
            self._logger.warning('No event handlers registered, event bus will not listen')
            return
        await self._pubsub.subscribe(*channels)
        self._listen_task = asyncio.create_task(self._listen())
        self._logger.info(
            f'Event bus started, listening on {len(channels)} channels',
            extra={'channels': channels}
        )

    async def stop(self) -> None:
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                self._logger.debug('Listen task cancelled')
        if self._pubsub:
            await self._pubsub.unsubscribe()
            await self._pubsub.close()
        self._listen_task = None
        self._pubsub = None
        self._logger.info('Event bus stopped')

    async def _listen(self) -> None:
        try:
            await self._listen_loop()
        except asyncio.CancelledError:
            self._logger.debug('Listen loop cancelled')
            raise
        except Exception as e:
            self._logger.exception(f'Error in listen loop: {e}')
            raise

    async def _listen_loop(self) -> None:
        async for message in self._pubsub.listen():
            if message['type'] == 'message':
                await self._handle_message(message)

    async def _handle_message(self, message: dict) -> None:
        try:
            channel = message['channel'].decode()
        except Exception as e:
            self._logger.exception(f'Failed to decode channel: {e}')
            return
        event_type = channel.replace(f'{self._channel_prefix}:', '')
        try:
            event = self._registry.deserialize(event_type, message['data'])
        except Exception as e:
            self._logger.exception(
                f'Failed to deserialize event {event_type}: {e}'
            )
            return
        handlers = self._handlers.get(event_type, [])
        if not handlers:
            self._logger.warning(
                f'No handlers registered for event {event_type}',
                extra={'event_id': str(event.event_id)}
            )
            return
        self._logger.debug(
            f'Handling event {event_type} with {len(handlers)} handlers',
            extra={'event_id': str(event.event_id)}
        )
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                self._logger.exception(
                    f'Error in handler for event {event_type}: {e}',
                    extra={'event_id': str(event.event_id)},
                )
