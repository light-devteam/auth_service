from datetime import datetime
from uuid import UUID

from msgspec import Struct


class AppDTO(Struct):
    id: UUID
    account_id: UUID
    name: str
    created_at: datetime
    description: str = ''
    deleted_at: datetime | None = None
