from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.enums import JwtAlgorithms


class Settings(BaseSettings):
    JWT_ACCESS_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_EXPIRE_DAYS: int = 30
    JWT_ALGORITHM: JwtAlgorithms = JwtAlgorithms.RS256
    JWT_PRIVATE_KEY: str = Path('keys/private.pem').read_text()
    JWT_PUBLIC_KEY: str = Path('keys/public.pem').read_text()

    LOGS_FILE: str = 'logs.log'
    DEV_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )


settings = Settings()
