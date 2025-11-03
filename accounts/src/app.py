from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, HTTPException
import uvicorn

from config import logger
from src.exceptions import AccountsBaseException
from src.api import router as api_router
from src.storages import postgres


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
            title='Accounts Service',
            docs_url='/swagger',
            lifespan=self.lifespan,
        )
        self.__api.add_exception_handler(AccountsBaseException, self.exception_handler)
        self.__api.include_router(api_router)
        self.__host = host
        self.__port = port
        self.__workers = workers
        App.__initiated = True

    def exception_handler(self, request: Request, exception: AccountsBaseException) -> None:
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
        logger.info('App started')
        yield
        await postgres.disconnect()
        logger.info('App finished')

    @property
    def api(self) -> FastAPI:
        return self.__api
