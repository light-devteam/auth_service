from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateAppRequestSchema(BaseModel):
    account_id: UUID
    name: str = Field(min_length=1, max_length=64)
    description: Optional[str] = Field('', max_length=255)
