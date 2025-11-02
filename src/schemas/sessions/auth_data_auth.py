from pydantic import BaseModel

from src.schemas.sessions.telegram_auth_data import TelegramAuthDataSchema
from src.schemas.sessions.fingerprint import FingerprintSchema


class TelegramAuthDataAuthSchema(BaseModel):
    telegram_auth_data: TelegramAuthDataSchema = None
    fingerprint: FingerprintSchema
