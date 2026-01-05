from typing import Any, Union
import json

from pydantic import BaseModel, Field, field_validator

from src.contexts.authentication.domain.value_objects.enums import ProviderType
from src.contexts.authentication.delivery.http.providers.schemas.provider_configs import (
    PasswordProviderConfig,
    TelegramProviderConfig,
)
from src.delivery.validators import validate_raw_json



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
        max_size_bytes = 2 * 1024  #  2 KB
        max_top_level_keys = 20
        max_depth = 10
        return validate_raw_json(value, max_size_bytes, max_top_level_keys, max_depth)
