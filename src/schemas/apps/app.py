from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AppSchema(BaseModel):
    id: UUID
    account_id: UUID
    name: str = Field(min_length=1, max_length=64)
    description: str = Field(max_length=255)
    created_at: datetime
    deleted_at: Optional[datetime] = None
