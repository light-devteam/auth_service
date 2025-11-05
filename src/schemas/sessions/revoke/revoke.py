from uuid import UUID

from pydantic import BaseModel


class RevokeSessionSchema(BaseModel):
    account_id: UUID
    session_id: UUID
