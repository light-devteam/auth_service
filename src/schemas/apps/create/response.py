from uuid import UUID

from pydantic import BaseModel


class CreateAppResponseSchema(BaseModel):
    id: UUID
