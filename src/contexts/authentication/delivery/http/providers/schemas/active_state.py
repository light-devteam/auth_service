from uuid import UUID

from pydantic import BaseModel


class ActiveState(BaseModel):
    id: UUID
    is_active: bool
