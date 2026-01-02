from datetime import datetime, timezone
from typing import Optional

from msgspec import Struct

from src.domain.value_objects.id import AccountID
from src.contexts.authentication.domain.value_objects import SessionID, ProviderID
from src.contexts.authentication.domain.exceptions import SessionAlreadyRevoked
from src.contexts.authentication.domain.entities.refresh_token import RefreshToken


class Session(Struct, kw_only=True):
    id: SessionID
    account_id: AccountID
    provider_id: ProviderID
    created_at: datetime
    revoked_at: Optional[datetime] = None

    refresh_token: RefreshToken

    def revoke(self) -> None:
        if self.revoked_at is None:
            try:
                self.refresh_token.revoke()
            finally:
                self.revoked_at = self.refresh_token.revoked_at
        raise SessionAlreadyRevoked()

    def is_active(self) -> bool:
        not_revoked = self.revoked_at is None
        token_active = self.refresh_token.is_active()
        return not_revoked and token_active
