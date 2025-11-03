from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator
from jwt import PyJWK


class Settings(BaseSettings):
    POSTGRES_URL: str
    REDIS_URL: str

    JWK_ENCRYPTION_KEY: SecretStr
    JWK_PRIVATE_KEY: PyJWK | None = None
    JWKS: dict[str, PyJWK] | None = None

    ACCOUNTS_SERVICE_URL: str
    COOKIE_DOMAIN: str
    VERIFY_AUTH_DATA_URL: str

    VERIFY_INIT_DATA_URLS: str | dict[str, str]

    CORS_ALLOW_ORIGINS: str | list[str] = '*'

    LOGS_FILE: str = 'logs.log'
    DEV_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )

    @field_validator('VERIFY_INIT_DATA_URLS', mode='before')
    def validate_verify_init_data_urls(cls, value: Any) -> Any | dict[str, str]:
        if isinstance(value, str):
            pairs = dict()
            for pair in value.split('\n'):
                pair = pair.strip()
                if not pair:
                    continue
                try:
                    bot_name, url = pair.split('=', 1)
                except:
                    continue
                pairs[bot_name.strip()] = url.strip()
            return pairs
        return value

    @field_validator('CORS_ALLOW_ORIGINS', mode='before')
    def validate_cors_allow_origins(cls, value: Any) -> Any | dict[str, str]:
        if isinstance(value, str):
            if value == '*':
                return value
            urls = []
            for url in value.split('\n'):
                url = url.strip()
                if not url:
                    continue
                urls.append(url)
            return urls
        return value

    def set_private_key(self, new_key: PyJWK) -> None:
        self.JWK_PRIVATE_KEY = new_key

    def set_jwks(self, new_jwks: dict[str, PyJWK]) -> None:
        self.JWKS = new_jwks


settings = Settings()
