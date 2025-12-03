from uuid import UUID

from msgspec import Struct

from src.enums import AppTypes


class AppDTO(Struct):
    id: UUID
    account_id: UUID
    name: str
    description: str
    type: AppTypes
