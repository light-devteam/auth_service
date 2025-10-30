from datetime import datetime

from msgspec import Struct


class AccessTokenDTO(Struct):
    token: str
    issued_at: datetime
    expires_at: datetime
