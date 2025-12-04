from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AppTokenMetaSchema(BaseModel):
    id: UUID
    app_id: UUID
    name: str = Field(min_length=1, max_length=64)
    created_at: datetime
    expires_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None
