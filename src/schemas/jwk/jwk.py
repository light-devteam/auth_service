from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_serializer


class JWKSchema(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=255)
    is_active: bool
    created_at: datetime

    @field_serializer('created_at', when_used='json-unless-none')
    def serialize_datetime(self, value: datetime) -> float:
        return value.timestamp()
