from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Account(BaseModel):
    id: UUID
    identities: Optional[list] = Field(None)
