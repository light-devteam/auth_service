from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, HTTPException
import uvicorn

from config import logger
from src.exceptions import AuthBaseException, JWKNotFoundException
from src.api import router as api_router
from src.well_known import router as well_known_router
from src.storages import postgres, redis
from src.services import JWKeysService
from src.middlewares import IPMiddleware


class App:
    __instance = None
    __initiated = False

    def __new__(cls, *args: list, **kwargs: dict) -> None:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self,
        host: str = '127.0.0.1',
        port: int = 8000,
        workers: int = 1,
    ) -> None:
        if App.__initiated:
            logger.warning('App already initated!')
            return
        self.__api = FastAPI(
            title='Auth Service',
            docs_url='/swagger',
            lifespan=self.lifespan,
        )
        self.__api.add_exception_handler(AuthBaseException, self.exception_handler)
        self.__include_middlewares()
        self.__api.include_router(well_known_router)
        self.__api.include_router(api_router)
        self.__host = host
        self.__port = port
        self.__workers = workers
        App.__initiated = True

    def exception_handler(self, request: Request, exception: AuthBaseException) -> None:
        raise HTTPException(
            status_code=exception._STATUS_CODE,
            detail=exception._DETAIL,
        )

    def run(self) -> None:
        uvicorn.run(
            app=self.__api,
            host=self.__host,
            port=self.__port,
            workers=self.__workers,
            access_log=False,
        )

    @asynccontextmanager
    async def lifespan(self, api: FastAPI) -> AsyncGenerator[None, None]:
        await postgres.connect()
        await redis.connect()
        await self.initialize_jwk()
        logger.info('App started')
        yield
        await postgres.disconnect()
        await redis.disconnect()
        logger.info('App finished')

    @property
    def api(self) -> FastAPI:
        return self.__api

    async def initialize_jwk(self) -> None:
        try:
            await JWKeysService.set_private_key_to_config()
        except JWKNotFoundException:
            jwk_id = await JWKeysService.create_key('main')
            await JWKeysService.set_primary(jwk_id)
            await JWKeysService.set_private_key_to_config()
        await JWKeysService.set_jwks_to_config()

    def __include_middlewares(self) -> None:
        self.__api.add_middleware(IPMiddleware)
