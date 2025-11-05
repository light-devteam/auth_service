from uuid import UUID

from pydantic import BaseModel


class RevokeAllSessionsSchema(BaseModel):
    account_id: UUID
