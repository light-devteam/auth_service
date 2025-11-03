from aiogram.utils.web_app import WebAppInitData
import httpx
from fastapi import status

from src.exceptions import AuthBaseException, InvalidInitDataException,BotNameDoesNotExist
from src.dto import TelegramAuthDataDTO
from config import settings, logger
from package.msgspec_json import json_encoder


class Telegram:
    @classmethod
    async def verify_init_data(cls, init_data: WebAppInitData, bot_name: str) -> None:
        verify_init_data_url = await cls.get_verify_init_data_url(bot_name)
        async with httpx.AsyncClient() as client:
            try:
                check_data_result = await client.post(
                    verify_init_data_url,
                    json={'init_data': init_data.model_dump_json()},
                )
            except httpx.HTTPError:
                raise AuthBaseException()
        if check_data_result.status_code == status.HTTP_401_UNAUTHORIZED:
            raise InvalidInitDataException()

    async def verify_auth_data(auth_data: TelegramAuthDataDTO) -> None:
        verify_data_url = settings.VERIFY_AUTH_DATA_URL
        async with httpx.AsyncClient() as client:
            try:
                check_data_result = await client.post(
                    verify_data_url,
                    json=json_encoder.encode(auth_data).decode('utf-8'),
                )
            except httpx.HTTPError as exception:
                logger.error(exception)
                raise AuthBaseException()
        if check_data_result.status_code == status.HTTP_401_UNAUTHORIZED:
            raise InvalidInitDataException()

    @classmethod
    async def get_verify_init_data_url(cls, bot_name: str) -> str:
        try:
            return settings.VERIFY_INIT_DATA_URLS[bot_name]
        except KeyError:
            logger.error(f'Bot key `{bot_name}` does not exists')
            raise BotNameDoesNotExist()
