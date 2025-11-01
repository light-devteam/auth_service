from uuid import UUID

from pydantic import BaseModel


class ResponseCreateJWKSchema(BaseModel):
    id: UUID
