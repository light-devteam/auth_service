from datetime import datetime
from uuid import UUID

from src.dao import SessionsRedisDAO
from src.dto import DeviceInfoDTO


class SessionsRepository:
    @classmethod
    async def add_session(
        cls,
        account_id: UUID,
        token_hash: str,
        device_info: DeviceInfoDTO,
        expires_at: datetime,
        issued_at: datetime,
    ) -> None:
        await SessionsRedisDAO.add_session(
            account_id,
            token_hash,
            device_info,
            expires_at,
            issued_at,
        )
