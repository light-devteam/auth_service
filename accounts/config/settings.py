from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_URL: str

    LOGS_FILE: str = 'logs.log'
    DEV_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )


settings = Settings()
