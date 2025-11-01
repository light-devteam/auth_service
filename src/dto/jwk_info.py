from uuid import UUID
from datetime import datetime

from msgspec import Struct


class JWKInfoDTO(Struct):
    id: UUID
    name: str
    is_active: bool
    created_at: datetime
