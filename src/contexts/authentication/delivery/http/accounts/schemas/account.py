from uuid import UUID

from pydantic import BaseModel


class Account(BaseModel):
    id: UUID
