from typing import Mapping

from src.contexts.jwk.domain.entities import JWKToken
from src.contexts.jwk.domain.value_objects import (
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

    def from_entity(self, entity: JWKToken) -> Mapping:
        return {
            'id': str(entity.id),
            'name': str(entity.name),
            'public': entity.public,
            'private': entity.private.get_secret_value(),
            'is_active': entity.is_active,
            'is_primary': entity.is_primary,
            'created_at': entity.created_at.timestamp(),
        }
