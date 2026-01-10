from typing import Mapping, Any

from src.contexts.authentication.domain import entities, value_objects


class RefreshTokenMapper:
    def to_entity(self, raw: Mapping[str, Any]) -> entities.RefreshToken:
        return entities.RefreshToken(
            id=value_objects.RefreshTokenID(raw['id']),
            session_id=value_objects.SessionID(raw['session_id']),
            hash=raw['hash'],
            created_at=raw['created_at'],
            expires_at=raw['expires_at'],
            revoked_at=raw.get('revoked_at', None),
        )
