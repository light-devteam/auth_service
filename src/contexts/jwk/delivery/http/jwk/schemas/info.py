from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_serializer

from src.contexts.jwk.delivery.http.jwk.schemas.public import JWKPublic


class JWKInfo(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=255)
    public: JWKPublic
    is_active: bool
    is_primary: bool
    created_at: datetime

    @field_serializer('created_at', when_used='json')
    def serialize_datetime(self, value: datetime) -> float:
        return value.timestamp()
