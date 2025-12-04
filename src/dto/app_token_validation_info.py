from uuid import UUID

from msgspec import Struct


class AppTokenValidationInfoDTO(Struct):
    app_id: UUID
    hash: str
