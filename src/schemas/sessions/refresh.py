from uuid import UUID

from pydantic import BaseModel


class RefreshSessionSchema(BaseModel):
    session_id: UUID
    refresh_token: str
