from typing import Union, Any

from pydantic import BaseModel, field_validator

from src.contexts.authentication.domain.value_objects import ProviderType
from src.contexts.authentication.delivery.http.auth.schemas.provider_credentials import (
    PasswordProviderCredentials,
    TelegramProviderCredentials,
)
from src.delivery.validators import validate_raw_json


class GetToken(BaseModel):
    provider_type: ProviderType
    credentials: Union[
        dict[str, Any],
        PasswordProviderCredentials,
        TelegramProviderCredentials,
    ] = {}

    @field_validator('credentials')
    @classmethod
    def validate_credentials(cls, value: dict[str, Any]) -> dict[str, Any]:
        max_size_bytes = 0.5 * 1024  #  0.5 KB
        max_top_level_keys = 6
        max_depth = 2
        return validate_raw_json(value, max_size_bytes, max_top_level_keys, max_depth)
