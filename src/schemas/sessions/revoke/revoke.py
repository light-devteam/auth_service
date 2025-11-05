from uuid import UUID

from pydantic import BaseModel


class RevokeSessionSchema(BaseModel):
    session_id: UUID
