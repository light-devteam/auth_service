from uuid import UUID
from typing import Literal, Optional, Any
from datetime import datetime

from pydantic import BaseModel, Field, field_serializer


class Provider(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=255)
    type: Literal['telegram']
    is_active: bool
    created_at: datetime
    config: Optional[dict[str, Any]] = None

    @field_serializer('created_at', when_used='json')
    def serialize_datetime(self, value: datetime) -> float:
        return value.timestamp()
