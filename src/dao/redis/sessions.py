from datetime import datetime, timezone
from uuid import UUID
from typing import Any

from src.storages import redis
from src.exceptions import MaximumSessionsCreatedException, SessionDoesNotExistsException
from src.dto import DeviceInfoDTO


class SessionsRedisDAO:
    MAX_SESSIONS_PER_ACCOUNT = 10

    @classmethod
    async def remove_expired_sessions(
        cls,
        account_id: UUID,
    ) -> None:
        account_key = cls.__get_account_key(account_id)
        current_ts = int(datetime.now(tz=timezone.utc).timestamp())
        await redis.connection.zremrangebyscore(account_key, 0, current_ts)

    @classmethod
    async def get_session_account_id(
        cls,
        token_hash: str,
    ) -> UUID:
        token_pattern = cls.__get_token_key('*', token_hash)
        keys = await redis.connection.keys(token_pattern)
        if not keys:
            raise SessionDoesNotExistsException()
        token_key = keys[0]
        account_id: bytes = token_key.split(b':')[1]
        return UUID(account_id.decode('utf-8'))

    @classmethod
    async def get_session(
        cls,
        token_hash: str,
        account_id: UUID | None = None,
    ) -> dict[str, Any]:
        if account_id is None:
            account_id = await cls.get_session_account_id(token_hash)
        token_key = cls.__get_token_key(account_id, token_hash)
        return await redis.connection.hgetall(token_key)

    @classmethod
    async def get_ip(cls, account_id: UUID, token_hash: str) -> str:
        session = await cls.get_session(token_hash, account_id)
        if not session:
            raise SessionDoesNotExistsException()
        return session.get('ip')

    @classmethod
    async def get_sessions(
        cls,
        account_id: UUID,
    ) -> list[dict[str, Any]]:
        account_key = cls.__get_account_key(account_id)
        token_hashes = await redis.connection.zrange(account_key, 0, -1)
        sessions = []
        for token_hash in token_hashes:
            session = await cls.get_session(token_hash, account_id)
            if session:
                sessions.append(session)
        return sessions

    @classmethod
    async def add_session(
        cls,
        account_id: UUID,
        token_hash: str,
        device_info: DeviceInfoDTO,
        expires_at: datetime,
        issued_at: datetime,
    ) -> str:
        return await cls.__save_session(
            account_id=account_id,
            token_hash=token_hash,
            device_info=device_info,
            expires_at=expires_at,
            issued_at=issued_at,
            check_limit=True,
        )

    @classmethod
    async def delete_session(cls, account_id: UUID, token_hash: str) -> None:
        token_key = cls.__get_token_key(account_id, token_hash)
        account_key = cls.__get_account_key(account_id)
        async with redis.connection.pipeline(transaction=True) as pipe:
            await pipe.delete(token_key)
            await pipe.zrem(account_key, token_hash)
            await pipe.execute()

    @classmethod
    async def refresh_session(
        cls,
        account_id: UUID,
        old_token_hash: str,
        new_token_hash: str,
        device_info: DeviceInfoDTO,
        expires_at: datetime,
        issued_at: datetime,
    ) -> str:
        return await cls.__save_session(
            account_id=account_id,
            token_hash=new_token_hash,
            device_info=device_info,
            expires_at=expires_at,
            issued_at=issued_at,
            old_token_hash=old_token_hash,
        )

    @classmethod
    async def revoke_all_sessions(
        cls,
        account_id: UUID,
    ) -> None:
        account_key = cls.__get_account_key(account_id)
        redis_lock_key = cls.__get_lock_key(account_id)
        redis_lock = redis.connection.lock(redis_lock_key, timeout=5, blocking_timeout=2)
        async with redis_lock:
            token_hashes = await redis.connection.zrange(account_key, 0, -1)
            async with redis.connection.pipeline(transaction=True) as pipe:
                for token_hash in token_hashes:
                    token_key = cls.__get_token_key(account_id, token_hash)
                    await pipe.delete(token_key)
                await pipe.delete(account_key)
                await pipe.execute()

    @classmethod
    async def revoke_other_sessions(
        cls,
        account_id: UUID,
        keep_token_hash: str,
    ) -> None:
        account_key = cls.__get_account_key(account_id)
        redis_lock_key = cls.__get_lock_key(account_id)
        redis_lock = redis.connection.lock(redis_lock_key, timeout=5, blocking_timeout=2)
        async with redis_lock:
            token_hashes = await redis.connection.zrange(account_key, 0, -1)
            async with redis.connection.pipeline(transaction=True) as pipe:
                for token_hash in token_hashes:
                    if token_hash == keep_token_hash:
                        continue
                    token_key = cls.__get_token_key(account_id, token_hash)
                    await pipe.delete(token_key)
                    await pipe.zrem(account_key, token_hash)
                await pipe.execute()

    @classmethod
    async def revoke_session(
        cls,
        account_id: UUID,
        token_hash: str,
    ) -> None:
        session = await cls.get_session(token_hash, account_id)
        if not session:
            raise SessionDoesNotExistsException()
        await cls.delete_session(account_id, token_hash)

    @classmethod
    async def __save_session(
        cls,
        account_id: UUID,
        token_hash: str,
        device_info: DeviceInfoDTO,
        expires_at: datetime,
        issued_at: datetime,
        old_token_hash: str | None = None,
        check_limit: bool = False,
    ) -> str:
        account_key = cls.__get_account_key(account_id)
        token_key = cls.__get_token_key(account_id, token_hash)
        expires_timestamp = int(expires_at.timestamp())
        issued_timestamp = int(issued_at.timestamp())
        session_ttl = expires_timestamp - int(datetime.now(tz=timezone.utc).timestamp())
        session_data = {
            'token_hash': token_hash,
            'ip': device_info.ip,
            'expires_at': expires_timestamp,
            'issued_at': issued_timestamp,
        }
        redis_lock_key = cls.__get_lock_key(account_id)
        redis_lock = redis.connection.lock(redis_lock_key, timeout=5, blocking_timeout=2)
        async with redis_lock:
            if check_limit:
                await cls.remove_expired_sessions(account_id)
                current_sessions = await cls.get_sessions(account_id)
                if len(current_sessions) >= cls.MAX_SESSIONS_PER_ACCOUNT:
                    raise MaximumSessionsCreatedException()
            async with redis.connection.pipeline(transaction=True) as pipe:
                if old_token_hash:
                    old_token_key = cls.__get_token_key(account_id, old_token_hash)
                    await pipe.delete(old_token_key)
                    await pipe.zrem(account_key, old_token_hash)
                await pipe.zadd(account_key, {token_hash: expires_timestamp})
                await pipe.hset(token_key, mapping=session_data)
                await pipe.expire(token_key, session_ttl)
                await pipe.execute()
            await cls.__update_account_key_ttl(account_key, session_ttl)
        return account_key

    @classmethod
    async def __update_account_key_ttl(
        cls,
        account_key: str,
        session_ttl: int,
    ) -> None:
        existing_ttl = await redis.connection.ttl(account_key)
        if existing_ttl < session_ttl:
            await redis.connection.expire(account_key, session_ttl)

    @classmethod
    def __get_account_key(cls, account_id: UUID | str) -> str:
        return f'refresh:{account_id}:tokens'

    @classmethod
    def __get_token_key(cls, account_id: UUID | str, token_hash: str) -> str:
        return f'refresh:{account_id}:token:{token_hash}'

    @classmethod
    def __get_lock_key(cls, account_id: UUID | str) -> str:
        return f'lock:refresh:{account_id}'
