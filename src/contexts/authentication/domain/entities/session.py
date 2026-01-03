from datetime import datetime, timezone
from typing import Optional, Self

from msgspec import Struct

from src.domain.value_objects.id import AccountID
from src.contexts.authentication.domain.value_objects import SessionID, ProviderID
from src.contexts.authentication.domain.exceptions import SessionAlreadyRevoked


class Session(Struct, kw_only=True):
    id: SessionID
    account_id: AccountID
    provider_id: ProviderID
    created_at: datetime
    revoked_at: Optional[datetime] = None

    @classmethod
    def create(cls, account_id: AccountID, provider_id: ProviderID) -> 'Session':
        return Session(
            id=SessionID.generate(),
            account_id=account_id,
            provider_id=provider_id,
            created_at=datetime.now(tz=timezone.utc),
            revoked_at=None,
        )

    def revoke(self) -> None:
        if not self.revoked_at:
            self.revoked_at = True
        raise SessionAlreadyRevoked()

    def is_active(self) -> bool:
        not_revoked = not self.revoked_at
        return not_revoked
