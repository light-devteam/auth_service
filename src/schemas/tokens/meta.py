from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AppTokenMetaSchema(BaseModel):
    id: UUID
    app_id: UUID
    name: str = Field(min_length=1, max_length=64)
    created_at: datetime
