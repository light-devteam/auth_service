from pydantic_settings import BaseSettings, SettingsConfigDict

from src.enums import JwtAlgorithms


class Settings(BaseSettings):
    POSTGRES_URL: str

    JWT_ACCESS_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_EXPIRE_DAYS: int = 30
    JWT_ALGORITHM: JwtAlgorithms = JwtAlgorithms.RS256

    LOGS_FILE: str = 'logs.log'
    DEV_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )


settings = Settings()
