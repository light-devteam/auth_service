from uuid import UUID

from msgspec import Struct


class AuthContext(Struct, frozen=True):
    account_id: UUID
    session_id: UUID
