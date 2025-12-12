from datetime import datetime, timezone
from typing import Self

from msgspec import Struct
from jwcrypto import jwk

from src.jwk.domain.value_objects import (
    JWKTokenID,
    JWKTokenName,
    JWKTokenPublic,
    JWKTokenPrivate,
)
from src.jwk.domain.exceptions import JWKCannotDeactivatePrimary
from src.domain.value_objects.enums import JWTAlgorithms


class JWKToken(Struct):
    id: JWKTokenID
    name: JWKTokenName
    public: JWKTokenPublic
    private: JWKTokenPrivate
    is_active: bool
    is_primary: bool
    created_at: datetime

    @classmethod
    def generate(cls, name: str) -> Self:
        key_id = JWKTokenID.generate()
        key = jwk.JWK.generate(
            kty='RSA',
            size=2048,
            alg=JWTAlgorithms.RS256.value,
            use='sig',
            kid=str(key_id),
        )
        return JWKToken(
            id=key_id,
            name=JWKTokenName(name),
            public=JWKTokenPublic(key.export_public(as_dict=True)),
            private=JWKTokenPrivate.create(key.export_private()),
            is_active=False,
            is_primary=False,
            created_at=datetime.now(tz=timezone.utc),
        )

    def toggle_active(self) -> None:
        if self.is_primary:
            raise JWKCannotDeactivatePrimary()
        self.is_active = not self.is_active

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        if self.is_primary:
            raise JWKCannotDeactivatePrimary()
        self.is_active = False
