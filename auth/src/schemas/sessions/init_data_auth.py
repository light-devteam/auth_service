from typing import Any

from pydantic import BaseModel, field_validator
from aiogram.utils.web_app import WebAppInitData, parse_webapp_init_data

from src.schemas.sessions.fingerprint import FingerprintSchema


class TelegramInitDataAuthSchema(BaseModel):
    telegram_init_data: WebAppInitData
    bot_name: str
    fingerprint: FingerprintSchema

    @field_validator('telegram_init_data', mode='before')
    def parse_telegram_init_data(cls, value: Any) -> Any | WebAppInitData:
        if isinstance(value, str):
            try:
                return parse_webapp_init_data(value)
            except Exception as e:
                raise ValueError(f'Invalid telegram_init_data: {e}')
        return value
