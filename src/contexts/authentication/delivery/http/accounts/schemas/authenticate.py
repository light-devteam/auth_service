from typing import Union, Any

from pydantic import BaseModel

from src.contexts.authentication.domain.value_objects import ProviderType


class AuthenticateRequest(BaseModel):
    provider_type: ProviderType
    credentials: Union[
        dict[str, Any],
    ] = {}
