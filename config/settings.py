from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_URL: str
    REDIS_URL: str

    CORS_ALLOW_ORIGINS: List[str] = ['*']

    LOGS_FILE: str = 'logs.log'
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
        case_sensitive=True,
    )
