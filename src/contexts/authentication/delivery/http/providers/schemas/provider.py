from uuid import UUID
from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel, Field, field_serializer

from src.contexts.authentication.domain.value_objects.enums import ProviderType


class Provider(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=255)
    type: ProviderType
    is_active: bool
    created_at: datetime
    config: dict[str, Any] = '{}'

    @field_serializer('created_at', when_used='json')
    def serialize_datetime(self, value: datetime) -> float:
        return value.timestamp()
