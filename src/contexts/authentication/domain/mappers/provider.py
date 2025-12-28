from typing import Mapping, Any

import json

from src.contexts.authentication.domain.entities import Provider
from src.contexts.authentication.domain.value_objects import ProviderID, ProviderName, ProviderType


class ProviderMapper:
    def to_entity(self, raw: Mapping[str, Any]) -> Provider:
        config = raw.get('config', None)
        if config is not None and not isinstance(config, dict):
            config = json.loads(config)
        return Provider(
            id=ProviderID(raw['id']),
            name=ProviderName(raw['name']),
            type=ProviderType(raw['type']),
            is_active=raw.get('is_active', False),
            created_at=raw['created_at'],
            config=config,
        )
