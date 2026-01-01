from datetime import datetime, timezone
from typing import Self, Any

from msgspec import Struct

from src.domain.value_objects import AccountID
from src.contexts.authentication.domain.value_objects import IdentityID, ProviderID


class Identity(Struct):
    id: IdentityID
    account_id: AccountID
    provider_id: ProviderID
    provider_data: dict[str, Any]
    created_at: datetime
    last_used_at: datetime

    @classmethod
    def create(
        cls,
        account_id: AccountID,
        provider_id: ProviderID,
        provider_data: dict[str, Any],
    ) -> Self:
        now = datetime.now(tz=timezone.utc)
        return Identity(
            id=IdentityID.generate(),
            account_id=account_id,
            provider_id=provider_id,
            provider_data=provider_data,
            created_at=now,
            last_used_at=now,
        )

    def update_last_used(self, last_used_at: datetime | None = None) -> None:
        if last_used_at is None:
            last_used_at = datetime.now(tz=timezone.utc)
        if last_used_at.tzinfo is None:
            last_used_at = last_used_at.replace(tzinfo=timezone.utc)
        self.last_used_at = last_used_at
