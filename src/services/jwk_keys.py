from uuid import UUID
import json

from jwt import PyJWK

from src.repositories import JWKeysRepository
from src.dto import JWKInfoDTO, JWKSDTO
from package import JWK
from config import settings


class JWKeysService:
    @classmethod
    async def get_key(cls, id: UUID) -> JWKInfoDTO:
        return await JWKeysRepository.get_key(id)

    @classmethod
    async def get_keys(cls, page: int = 1, page_size: int = 100) -> list[JWKInfoDTO]:
        return await JWKeysRepository.get_keys(page, page_size)

    @classmethod
    async def get_active_keys(cls, page: int = 1, page_size: int = 100) -> list[JWKInfoDTO]:
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

    @classmethod
    async def get_jwks(cls, page: int = 1, page_size: int = 100) -> JWKSDTO:
        return await JWKeysRepository.get_jwks(page, page_size)

    @classmethod
    async def set_primary(cls, id: UUID) -> None:
        return await JWKeysRepository.set_primary(id)

    @classmethod
    async def set_private_key_to_config(cls) -> None:
        jwk_private_key_encoded = await JWKeysRepository.get_primary_private()
        jwk_private_key = JWK.fernet_decrypt(jwk_private_key_encoded)
        settings.set_private_key(PyJWK.from_dict(jwk_private_key))

    @classmethod
    async def set_jwks_to_config(cls) -> None:
        page = 1
        jwks = dict()
        LOAD_JWKS = True
        while LOAD_JWKS:
            loaded_jwks = await JWKeysRepository.get_jwks(page)
            if not loaded_jwks.keys:
                break
            processed_jwks = {jwk['kid']: PyJWK.from_dict(jwk) for jwk in loaded_jwks.keys}
            jwks.update(processed_jwks)
            page += 1
        settings.set_jwks(jwks)
