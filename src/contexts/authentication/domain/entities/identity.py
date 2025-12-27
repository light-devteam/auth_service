from datetime import datetime, timezone

from msgspec import Struct

from src.domain.value_objects.id import AccountID
from src.contexts.authentication.domain.value_objects import SessionID, ProviderID


class Identity(Struct):
    id: SessionID
    account_id: AccountID
    provider_id: ProviderID
    provider_data: dict
    is_main: bool
    created_at: datetime
    last_used_at: datetime

    def update_last_used(self) -> None:
        self.last_used_at = datetime.now(tz=timezone.utc)
