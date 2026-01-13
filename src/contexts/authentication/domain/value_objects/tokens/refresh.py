from datetime import datetime

from msgspec import Struct

from src.domain.value_objects import AccountID


class RefreshToken(Struct):
    token: str
    hash: bytes
    issued_at: datetime
    expires_at: datetime
    account_id: AccountID
