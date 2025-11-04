from datetime import datetime
from uuid import UUID

from msgspec import Struct

from src.dto.redis_token_data import RedisTokenDataDTO


class RedisSessionDTO(Struct):
    id: UUID
    account_id: UUID
    issued_at: datetime
    expires_at: datetime
    ips: list[str]
    token: RedisTokenDataDTO
