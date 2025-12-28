from uuid import UUID

from pydantic import BaseModel


class CreateProviderResponse(BaseModel):
    id: UUID
