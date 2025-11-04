from datetime import datetime

from msgspec import Struct


class RedisTokenDataDTO(Struct):
    hash: str
    ip: str
    issued_at: datetime
    expires_at: datetime
