from uuid import UUID
import json

from src.repositories import JWKeysRepository
from src.dto import JWKDTO
from package import JWK


class JWKeysService:
    @classmethod
    async def get_key(cls, id: UUID) -> JWKDTO:
        return await JWKeysRepository.get_key(id)

    @classmethod
    async def get_keys(cls, page: int = 1, page_size: int = 100) -> list[JWKDTO]:
        return await JWKeysRepository.get_keys(page, page_size)

    @classmethod
    async def get_active_keys(cls, page: int = 1, page_size: int = 100) -> list[JWKDTO]:
        return await JWKeysRepository.get_active_keys(page, page_size)

    @classmethod
    async def create_key(cls, name: str) -> UUID:
        key_pair = JWK.generate()
        encoded_private_key = JWK.fernet_encrypt(key_pair.private)
        return await JWKeysRepository.create_key(
            UUID(key_pair.public['kid']),
            name,
            json.dumps(key_pair.public),
            encoded_private_key,
        )

    @classmethod
    async def deactivate_key(cls, id: UUID) -> None:
        await JWKeysRepository.deactivate_key(id)

    @classmethod
    async def activate_key(cls, id: UUID) -> None:
        await JWKeysRepository.activate_key(id)
