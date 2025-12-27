from datetime import datetime, timezone
from typing import Optional

from msgspec import Struct

from src.contexts.authentication.domain.value_objects import SessionID, RefreshTokenID
from src.contexts.authentication.domain.exceptions import TokenAlreadyRevoked


class RefreshToken(Struct):
    id: RefreshTokenID
    session_id: SessionID
    hash: bytes
    created_at: datetime
    expires_at: datetime
    revoked_at: Optional[datetime] = None

    def revoke(self) -> None:
        if self.revoked_at is None:
            self.revoked_at = datetime.now(tz=timezone.utc)
        raise TokenAlreadyRevoked()

    def is_active(self) -> bool:
        now = datetime.now(tz=timezone.utc)
        not_revoked = self.revoked_at is None
        not_expired = self.expires_at > now
        return not_revoked and not_expired
