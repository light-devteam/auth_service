from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CreateTokenRequestSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    expires_at: Optional[datetime] = None

    @field_validator('expires_at')
    @classmethod
    def validate_expires_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v <= datetime.now(tz=timezone.utc):
            raise ValueError('expires_at must be greater than current time')
        return v
