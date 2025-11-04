from datetime import datetime
from uuid import UUID
from typing import Any

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

    @classmethod
    async def get_session(
        cls,
        token_hash: str,
        account_id: UUID | None = None,
    ) -> dict[str, Any]:
        return await SessionsRedisDAO.get_session(token_hash, account_id)

    @classmethod
    async def get_session_account_id(cls, token_hash: str) -> UUID:
        return await SessionsRedisDAO.get_session_account_id(token_hash)

    @classmethod
    async def refresh_session(
        cls,
        account_id: UUID,
        old_token_hash: str,
        new_token_hash: str,
        device_info: DeviceInfoDTO,
        expires_at: datetime,
        issued_at: datetime,
    ) -> None:
        await SessionsRedisDAO.refresh_session(
            account_id=account_id,
            old_token_hash=old_token_hash,
            new_token_hash=new_token_hash,
            device_info=device_info,
            expires_at=expires_at,
            issued_at=issued_at,
        )
