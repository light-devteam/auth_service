from collections import deque
from typing import Any, Union
import json

from pydantic import BaseModel, Field, field_validator

from src.contexts.authentication.domain.value_objects.enums import ProviderType
from src.contexts.authentication.delivery.http.providers.schemas.provider_configs import (
    PasswordProviderConfig,
    TelegramProviderConfig,
)



class CreateProviderRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: ProviderType
    config: Union[
        dict[str, Any],
        PasswordProviderConfig,
        TelegramProviderConfig,
    ] = {}

    @field_validator('type')
    @classmethod
    def validate_provider_type(cls, value: ProviderType) -> ProviderType:
        if value == ProviderType.UNKNOWN:
            raise ValueError('Provider type `unknown` not allowed for create')
        return value

    @field_validator('config')
    @classmethod
    def validate_config(cls, value: dict[str, Any]) -> dict[str, Any]:
        config_json = json.dumps(value)
        config_bytes = len(config_json.encode('utf8'))
        max_size_bytes = 2 * 1024  #  2 KB
        max_top_level_keys = 20
        max_depth = 10
        if config_bytes > max_size_bytes:
            raise ValueError(f'Config too large: {config_bytes} bytes (max {max_size_bytes})')
        if len(value) > max_top_level_keys:
            raise ValueError(f'Too many top-level keys: {len(value)} (max {max_top_level_keys})')

        def check_depth(obj: dict | list, max_depth: int) -> int:
            if not isinstance(obj, (dict, list)):
                return 0
            depth = 0
            q = deque([(obj, 1)])
            while q:
                node, node_depth = q.popleft()
                depth = max(depth, node_depth)
                if depth > max_depth:
                    raise ValueError(f'Max depth ({max_depth}) exceeded')
                if isinstance(node, dict):
                    for v in node.values():
                        if isinstance(v, (dict, list)):
                            q.append((v, node_depth + 1))
                elif isinstance(node, list):
                    for item in node:
                        if isinstance(item, (dict, list)):
                            q.append((item, node_depth + 1))
            return depth

        check_depth(value, max_depth)
        return value
