from base64 import b64encode, b64decode
from cryptography.fernet import Fernet
import json
from typing import Self

from dependency_injector.wiring import inject, Provide

from src.infrastructure.config import Settings


class JWKTokenPrivate(bytes):
    def __new__(cls, value: bytes | str) -> Self:
        """Конструктор восстановления.

        Args:
            value (bytes | str): уже зашифрованные данные в формате base64

        Returns:
            JWKTokenPrivate: self
        """
        if isinstance(value, str):
            value = value.encode('utf-8')
        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(secret)'

    @classmethod
    def create(
        cls,
        value: dict | str | bytes,
    ) -> Self:
        if isinstance(value, dict):
            value = json.dumps(value)
        if isinstance(value, str):
            value = value.encode('utf-8')
        data = cls.__encrypt(value)
        return cls(data)

    def get_secret_value(self) -> dict:
        data = self.__decrypt()
        return json.loads(data.decode('utf-8'))

    @classmethod
    @inject
    def __encrypt(
        cls,
        value: bytes,
        settings: Settings = Provide['infrastructure.settings'],
    ) -> bytes:
        encrypted = Fernet(settings.JWK_ENCRYPTION_KEY.get_secret_value()).encrypt(value)
        return b64encode(encrypted)

    @inject
    def __decrypt(self, settings: Settings = Provide['infrastructure.settings']) -> bytes:
        token = b64decode(self)
        return Fernet(settings.JWK_ENCRYPTION_KEY.get_secret_value()).decrypt(token)
