from uuid import UUID

from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: UUID
    telegram_id: int
