from uuid import UUID

from src.dao import SessionsRedisDAO
from src.dto import RedisTokenDataDTO, RedisSessionDTO


class SessionsRepository:
    @classmethod
    async def get_session(cls, session_id: UUID) -> RedisSessionDTO:
        return await SessionsRedisDAO.get_session(session_id)

    @classmethod
    async def add_session(
        cls,
        account_id: UUID,
        token_data: RedisTokenDataDTO,
    ) -> UUID:
        return await SessionsRedisDAO.add_session(account_id, token_data)

    @classmethod
    async def refresh_session(
        cls,
        session_id: UUID,
        account_id: UUID,
        token_data: RedisTokenDataDTO,
    ) -> UUID:
        return await SessionsRedisDAO.refresh_session(
            session_id=session_id,
            account_id=account_id,
            token_data=token_data,
        )

    @classmethod
    async def revoke(cls, session_id: UUID) -> None:
        return await SessionsRedisDAO.revoke(session_id)

    @classmethod
    async def revoke_all(cls, account_id: UUID) -> None:
        return await SessionsRedisDAO.revoke_all(account_id)

    @classmethod
    async def revoke_other(cls, account_id: UUID, keep_session_id: UUID) -> None:
        return await SessionsRedisDAO.revoke_other(account_id, keep_session_id)
