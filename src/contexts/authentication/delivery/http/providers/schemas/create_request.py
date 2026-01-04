from typing import Optional, Any

from pydantic import BaseModel, Field

from src.contexts.authentication.domain.value_objects.enums import ProviderType


class CreateProviderRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: ProviderType
    config: Optional[dict[str, Any]] = None
