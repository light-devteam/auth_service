from uuid import UUID
from datetime import datetime

from msgspec import Struct


class AppTokenMetaDTO(Struct):
    id: UUID
    app_id: UUID
    name: str
    created_at: datetime
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
