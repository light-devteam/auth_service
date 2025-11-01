from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from jwt import PyJWK


class Settings(BaseSettings):
    POSTGRES_URL: str

    JWK_ENCRYPTION_KEY: SecretStr
    JWK_PRIVATE_KEY: PyJWK | None = None

    LOGS_FILE: str = 'logs.log'
    DEV_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )

    def set_private_key(self, new_key: PyJWK) -> None:
        self.JWK_PRIVATE_KEY = new_key


settings = Settings()
