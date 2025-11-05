from uuid import UUID

from pydantic import BaseModel


class RevokeOtherSessionsSchema(BaseModel):
    keep_session_id: UUID
