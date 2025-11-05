from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.storages import redis
from src.exceptions import MaximumSessionsCreatedException, SessionDoesNotExistsException
from src.dto import RedisTokenDataDTO, RedisSessionDTO


class SessionsRedisDAO:
    MAX_SESSIONS_PER_ACCOUNT = 10

    @classmethod
    async def remove_expired_sessions(cls, account_id: UUID) -> None:
        account_key = cls.__get_account_sessions_key(account_id)
        now_ts = int(datetime.now(tz=timezone.utc).timestamp())
        await redis.connection.zremrangebyscore(account_key, 0, now_ts)

    @classmethod
    async def get_session(cls, session_id: UUID) -> RedisSessionDTO:
        session_key = cls.__get_session_key(session_id)
        session_token_key = cls.__get_session_token_key(session_id)
        session_ips_key = cls.__get_session_ips_key(session_id)
        session_data = await redis.connection.hgetall(session_key)
        if not session_data:
            raise SessionDoesNotExistsException()
        session_token_data = await redis.connection.hgetall(session_token_key)
        if not session_token_data:
            raise SessionDoesNotExistsException()
        session_ips_data = await redis.connection.smembers(session_ips_key)
        ips_list = [ip.decode() if isinstance(ip, bytes) else str(ip) for ip in session_ips_data]
        token_dto = RedisTokenDataDTO(
            hash=session_token_data[b'hash'].decode('utf-8'),
            ip=session_token_data[b'ip'].decode('utf-8'),
            issued_at=datetime.fromtimestamp(float(session_token_data[b'issued_at']), tz=timezone.utc),
            expires_at=datetime.fromtimestamp(float(session_token_data[b'expires_at']), tz=timezone.utc),
        )
        return RedisSessionDTO(
            id=session_id,
            account_id=UUID(session_data[b'account_id'].decode('utf-8')),
            issued_at=datetime.fromtimestamp(float(session_data[b'issued_at']), tz=timezone.utc),
            expires_at=datetime.fromtimestamp(float(session_data[b'expires_at']), tz=timezone.utc),
            token=token_dto,
            ips=ips_list,
        )

    @classmethod
    async def get_sessions(cls, account_id: UUID) -> list[RedisSessionDTO]:
        account_sessions_key = cls.__get_account_sessions_key(account_id)
        sessions_ids: list[bytes] = await redis.connection.zrange(account_sessions_key, 0, -1)
        sessions = []
        for session_id in sessions_ids:
            session = await cls.get_session(session_id.decode('utf-8'))
            if session:
                sessions.append(session)
        return sessions

    @classmethod
    async def get_sessions_count(cls, account_id: UUID) -> int:
        account_sessions_key = cls.__get_account_sessions_key(account_id)
        return await redis.connection.zcard(account_sessions_key)

    @classmethod
    async def add_session(
        cls,
        account_id: UUID,
        token_data: RedisTokenDataDTO,
    ) -> UUID:
        session_id = uuid4()
        return await cls.__save_session(
            session_id=session_id,
            account_id=account_id,
            token_data=token_data,
        )

    @classmethod
    async def refresh_session(
        cls,
        session_id: UUID,
        account_id: UUID,
        token_data: RedisTokenDataDTO,
    ) -> UUID:
        return await cls.__save_session(
            session_id=session_id,
            account_id=account_id,
            token_data=token_data,
            is_update=True,
        )

    @classmethod
    async def revoke(cls, session_id: UUID) -> None:
        session = await cls.get_session(session_id)
        account_id = session.account_id
        account_sessions_key = cls.__get_account_sessions_key(account_id)
        session_key = cls.__get_session_key(session_id)
        session_token_key = cls.__get_session_token_key(session_id)
        session_ips_key = cls.__get_session_ips_key(session_id)
        async with redis.connection.pipeline(transaction=True) as pipe:
            await pipe.zrem(account_sessions_key, str(session_id))
            await pipe.delete(session_key)
            await pipe.delete(session_token_key)
            await pipe.delete(session_ips_key)
            await pipe.execute()

    @classmethod
    async def revoke_all(cls, account_id: UUID) -> None:
        account_sessions_key = cls.__get_account_sessions_key(account_id)
        sessions_ids: list[bytes] = await redis.connection.zrange(account_sessions_key, 0, -1)
        if not sessions_ids:
            return
        async with redis.connection.pipeline(transaction=True) as pipe:
            for session_id_bytes in sessions_ids:
                session_id = session_id_bytes.decode('utf-8')
                session_key = cls.__get_session_key(session_id)
                session_token_key = cls.__get_session_token_key(session_id)
                session_ips_key = cls.__get_session_ips_key(session_id)
                await pipe.delete(session_key)
                await pipe.delete(session_token_key)
                await pipe.delete(session_ips_key)
            await pipe.delete(account_sessions_key)
            await pipe.execute()

    @classmethod
    async def revoke_other(cls, account_id: UUID, keep_session_id: UUID) -> None:
        account_sessions_key = cls.__get_account_sessions_key(account_id)
        sessions_ids: list[bytes] = await redis.connection.zrange(account_sessions_key, 0, -1)
        if not sessions_ids:
            return
        async with redis.connection.pipeline(transaction=True) as pipe:
            for session_id_bytes in sessions_ids:
                session_id_str = session_id_bytes.decode('utf-8')
                if session_id_str == str(keep_session_id):
                    continue
                session_key = cls.__get_session_key(session_id_str)
                session_token_key = cls.__get_session_token_key(session_id_str)
                session_ips_key = cls.__get_session_ips_key(session_id_str)
                await pipe.zrem(account_sessions_key, session_id_str)
                await pipe.delete(session_key)
                await pipe.delete(session_token_key)
                await pipe.delete(session_ips_key)
            await pipe.execute()

    @classmethod
    async def __save_session(
        cls,
        session_id: UUID,
        account_id: UUID,
        token_data: RedisTokenDataDTO,
        is_update: bool = False,
    ) -> UUID:
        account_sessions_key = cls.__get_account_sessions_key(account_id)
        session_key = cls.__get_session_key(session_id)
        session_token_key = cls.__get_session_token_key(session_id)
        session_ips_key = cls.__get_session_ips_key(session_id)
        expires_timestamp = token_data.expires_at.timestamp()
        issued_timestamp = token_data.issued_at.timestamp()
        token_ttl = int(expires_timestamp - datetime.now(tz=timezone.utc).timestamp())
        token_data_dict = {
            'hash': token_data.hash,
            'ip': token_data.ip,
            'issued_at': issued_timestamp,
            'expires_at': expires_timestamp,
        }
        redis_lock_key = cls.__get_lock_key(account_id)
        redis_lock = redis.connection.lock(redis_lock_key, timeout=5, blocking_timeout=2)
        async with redis_lock:
            await cls.__check_sessions_limit(account_id)
            async with redis.connection.pipeline(transaction=True) as pipe:
                await pipe.zadd(account_sessions_key, {str(session_id): expires_timestamp})
                await pipe.hset(session_token_key, mapping=token_data_dict)
                if not is_update:
                    await pipe.hset(session_key, 'account_id', str(account_id))
                    await pipe.hset(session_key, 'issued_at', issued_timestamp)
                await pipe.hset(session_key, 'expires_at', expires_timestamp)
                await pipe.sadd(session_ips_key, token_data.ip)
                await pipe.expire(session_key, token_ttl)
                await pipe.expire(session_token_key, token_ttl)
                await pipe.expire(session_ips_key, token_ttl)
                await pipe.execute()
            await cls.__update_ttl(account_sessions_key, token_ttl)
        return session_id

    @classmethod
    async def __check_sessions_limit(cls, account_id: UUID) -> None:
        await cls.remove_expired_sessions(account_id)
        if await cls.get_sessions_count(account_id) >= cls.MAX_SESSIONS_PER_ACCOUNT:
            raise MaximumSessionsCreatedException()

    @classmethod
    async def __update_ttl(
        cls,
        key: str,
        ttl: int,
    ) -> None:
        existing_ttl = await redis.connection.ttl(key)
        if existing_ttl < ttl:
            await redis.connection.expire(key, ttl)

    @classmethod
    def __get_account_sessions_key(cls, account_id: UUID) -> str:
        return f'accounts:{account_id}:sessions'

    @classmethod
    def __get_session_key(cls, session_id: UUID) -> str:
        return f'sessions:{session_id}'

    @classmethod
    def __get_session_token_key(cls, session_id: UUID) -> str:
        session_key = cls.__get_session_key(session_id)
        return f'{session_key}:token'

    @classmethod
    def __get_session_ips_key(cls, session_id: UUID) -> str:
        session_key = cls.__get_session_key(session_id)
        return f'{session_key}:ips'

    @classmethod
    def __get_lock_key(cls, account_id: UUID | str) -> str:
        return f'lock:refresh:{account_id}'
