from uuid import UUID

from pydantic import BaseModel


class CreateIdentityResponse(BaseModel):
    id: UUID
