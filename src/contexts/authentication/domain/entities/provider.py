from datetime import datetime
from typing import Optional

from msgspec import Struct

from src.contexts.authentication.domain.value_objects import (
    ProviderID,
    ProviderName,
    ProviderType,
)
from src.contexts.authentication.domain.exceptions import ProviderNotActive


class Provider(Struct, frozen=True):
    id: ProviderID
    name: ProviderName
    type: ProviderType
    is_active: bool
    created_at: datetime
    config: Optional[dict] = None

    def ensure_active(self) -> None:
        if not self.is_active:
            raise ProviderNotActive()
