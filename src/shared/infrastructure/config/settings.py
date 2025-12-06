from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    POSTGRES_URL: str
    REDIS_URL: str

    CORS_ALLOW_ORIGINS: list[str] = ['*']

    LOGS_FILE: str = 'logs.log'
    ENVIRONMENT: Literal['development', 'staging', 'production'] = 'development'
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        case_sensitive=True,
    )

    @field_validator('CORS_ALLOW_ORIGINS')
    @classmethod
    def validate_cors(cls, v, info):
        if info.data.get('ENVIRONMENT') == 'production' and '*' in v:
            raise ValueError('Wildcard CORS not allowed in production')
        return v
