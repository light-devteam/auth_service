from uuid import UUID

from pydantic import BaseModel


class CreateAccountResponse(BaseModel):
    id: UUID
