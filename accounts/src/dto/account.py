from uuid import UUID

from msgspec import Struct


class AccountDTO(Struct):
    id: UUID
    telegram_id: int
