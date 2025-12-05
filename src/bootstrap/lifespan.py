from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

# from config import logger
# from src.storages import postgres, redis
# from src.services import JWKeysService
# from src.exceptions import JWKNotFoundException


class LifespanManager:
    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncGenerator[None, None]:
#         logger.info('Starting application...')
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
        # logger.info('Application started successfully')
        yield
#         logger.info('Shutting down application...')
#         try:
#             await self._disconnect_storages()
#         except Exception as e:
#             logger.error(f'Error during shutdown: {e}')
#         else:
#             logger.info('Application stopped successfully')
    
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
    
#     async def _initialize_jwk(self) -> None:
#         logger.debug('Initializing JWK keys...')
#         try:
#             await JWKeysService.set_private_key_to_config()
#         except JWKNotFoundException:
#             logger.warning('JWK key not found, creating new one...')
#             jwk_id = await JWKeysService.create_key('main')
#             await JWKeysService.set_primary(jwk_id)
#             await JWKeysService.set_private_key_to_config()
#             logger.info(f'New JWK key created with id: {jwk_id}')
#         else:
#             logger.info('Existing JWK key loaded')
#         await JWKeysService.set_jwks_to_config()
#         logger.info('JWK keys initialized successfully')
