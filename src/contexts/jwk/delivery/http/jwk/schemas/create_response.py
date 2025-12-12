from uuid import UUID

from pydantic import BaseModel


class CreateJWKResponse(BaseModel):
    id: UUID
