from uuid import UUID
from datetime import datetime

from msgspec import Struct


class JWKDTO(Struct):
    id: UUID
    name: str
    is_active: bool
    created_at: datetime
