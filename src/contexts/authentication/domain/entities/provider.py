from datetime import datetime, timezone
from typing import Optional, Self, Any

from msgspec import Struct

from src.contexts.authentication.domain.value_objects import (
    ProviderID,
    ProviderName,
    enums,
)
from src.contexts.authentication.domain.exceptions import ProviderNotActive


class Provider(Struct):
    id: ProviderID
    name: ProviderName
    type: enums.ProviderType
    is_active: bool
    created_at: datetime
    config: Optional[dict[str, Any]] = None

    @classmethod
    def create(
        cls,
        name: ProviderName,
        type: enums.ProviderType,
        config: Optional[dict] = None,
    ) -> Self:
        return Provider(
            id=ProviderID.generate(),
            name=name,
            type=type,
            is_active=False,
            created_at=datetime.now(tz=timezone.utc),
            config=config,
        )

    def ensure_active(self) -> None:
        if not self.is_active:
            raise ProviderNotActive()

    def toggle_active(self) -> bool:
        self.is_active = not self.is_active
        return self.is_active

    def activate(self) -> None:
        self.is_active = True
