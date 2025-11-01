import json
from base64 import b64encode, b64decode
from uuid import uuid4

from cryptography.fernet import Fernet
from jwcrypto import jwk

from config import settings
from src.dto import JWKPairDTO
from src.enums import JwtAlgorithms


class JWK:
    @classmethod
    def generate(cls) -> JWKPairDTO:
        key_id = uuid4()
        key = jwk.JWK.generate(
            kty='RSA',
            size=2048,
            alg=JwtAlgorithms.RS256.value,
            use='sig',
            kid=str(key_id),
        )
        return JWKPairDTO(
            public=key.export_public(as_dict=True),
            private=key.export_private(as_dict=True),
        )

    @classmethod
    def fernet_encrypt(cls, token: dict) -> bytes:
        data = json.dumps(token).encode('utf-8')
        encrypted_token = Fernet(settings.JWK_ENCRYPTION_KEY.get_secret_value()).encrypt(data)
        return b64encode(encrypted_token)

    @classmethod
    def fernet_decrypt(cls, token_b64: bytes) -> dict:
        token = b64decode(token_b64)
        data = Fernet(settings.JWK_ENCRYPTION_KEY.get_secret_value()).decrypt(token)
        return json.loads(data.decode('utf-8'))
