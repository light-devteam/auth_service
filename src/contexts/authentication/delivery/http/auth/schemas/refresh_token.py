from datetime import datetime

from pydantic import BaseModel, field_serializer


class RefreshToken(BaseModel):
    token: str
    issued_at: datetime
    expires_at: datetime

    @field_serializer('issued_at', 'expires_at', when_used='json')
    def serialize_datetime(self, value: datetime) -> float:
        return value.timestamp()
