from typing import Mapping, Any

import json

from src.domain.value_objects import AccountID
from src.contexts.authentication.domain import entities, value_objects


class IdentityMapper:
    def to_entity(self, raw: Mapping[str, Any]) -> entities.Identity:
        return entities.Identity(
            id=value_objects.IdentityID(raw['id']),
            account_id=AccountID(raw['account_id']),
            provider_id=value_objects.ProviderID(raw['provider_id']),
            credentials=json.loads(raw['credentials']),
            created_at=raw['created_at'],
            last_used_at=raw['last_used_at'],
        )
