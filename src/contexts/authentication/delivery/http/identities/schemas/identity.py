from uuid import UUID
from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_serializer


class Identity(BaseModel):
    id: UUID
    account_id: UUID
    provider_id: UUID
    credentials: dict[str, Any]
    is_main: bool
    created_at: datetime
    last_used_at: datetime

    @field_serializer('created_at', 'last_used_at', when_used='json')
    def serialize_datetime(self, value: datetime) -> float:
        return value.timestamp()
