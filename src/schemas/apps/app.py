from uuid import UUID

from pydantic import BaseModel, Field

from src.enums import AppTypes


class AppSchema(BaseModel):
    id: UUID
    account_id: UUID
    name: str = Field(min_length=1, max_length=64)
    description: str = Field(max_length=255)
    type: AppTypes
