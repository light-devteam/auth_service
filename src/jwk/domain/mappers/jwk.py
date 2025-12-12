from typing import Mapping

from src.jwk.domain.entities import JWKToken
from src.jwk.domain.value_objects import (
    JWKTokenID,
    JWKTokenName,
    JWKTokenPublic,
    JWKTokenPrivate,
)


class JWKMapper:
    def to_entity(self, raw: Mapping) -> JWKToken:
        return JWKToken(
            id=JWKTokenID(raw['id']),
            name=JWKTokenName(raw['name']),
            public=JWKTokenPublic(raw['public']),
            private=JWKTokenPrivate(raw['private']),
            is_active=raw['is_active'],
            is_primary=raw['is_primary'],
            created_at=raw['created_at'],
        )
