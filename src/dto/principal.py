from uuid import UUID

from msgspec import Struct

from src.enums import PrincipalTypes


class PrincipalDTO(Struct):
    id: UUID
    type: PrincipalTypes
