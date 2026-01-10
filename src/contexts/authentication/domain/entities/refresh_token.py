from datetime import datetime, timezone
from typing import Optional

from msgspec import Struct

from src.contexts.authentication.domain.value_objects import (
    SessionID,
    RefreshTokenID,
    RefreshToken as RefreshTokenDTO,
)
from src.contexts.authentication.domain.exceptions import TokenAlreadyRevoked


class RefreshToken(Struct):
    id: RefreshTokenID
    session_id: SessionID
    hash: bytes
    created_at: datetime
    expires_at: datetime
    revoked_at: Optional[datetime] = None

    @classmethod
    def create(cls, session_id: SessionID, token: RefreshTokenDTO) -> 'RefreshToken':
        return RefreshToken(
            id=RefreshTokenID.generate(),
            session_id=session_id,
            hash=token.token.encode('utf-8'),
            created_at=token.issued_at,
            expires_at=token.expires_at,
            revoked_at=None,
        )

    def revoke(self) -> None:
        if self.revoked_at is None:
            self.revoked_at = datetime.now(tz=timezone.utc)
        raise TokenAlreadyRevoked()

    def is_active(self) -> bool:
        now = datetime.now(tz=timezone.utc)
        not_revoked = self.revoked_at is None
        not_expired = self.expires_at > now
        return not_revoked and not_expired
