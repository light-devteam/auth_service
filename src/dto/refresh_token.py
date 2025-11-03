from datetime import datetime

from msgspec import Struct


class RefreshTokenDTO(Struct):
    token: str
    issued_at: datetime
    expires_at: datetime
    hash: str
