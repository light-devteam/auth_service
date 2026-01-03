from typing import Mapping, Any

from src.domain.value_objects import AccountID
from src.contexts.authentication.domain import entities, value_objects


class SessionMapper:
    def to_entity(self, raw: Mapping[str, Any]) -> entities.Session:
        return entities.Session(
            id=value_objects.SessionID(raw['id']),
            account_id=AccountID(raw['account_id']),
            provider_id=value_objects.ProviderID(raw['provider_id']),
            created_at=raw['created_at'],
            revoked_at=raw.get('revoked_at', None),
        )
