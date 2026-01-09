from datetime import datetime

from msgspec import Struct


class AccessToken(Struct):
    token: str
    issued_at: datetime
    expires_at: datetime
