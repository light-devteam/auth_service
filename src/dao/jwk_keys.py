from asyncpg import Connection, Record

from src.dao.base import BaseDAO


class JWKeysDAO(BaseDAO):
    _TABLE_NAME = 'jwk.keys'

    @classmethod
    async def get_jwks(
        cls,
        connection: Connection,
        page: int = 1,
        page_size: int = 100,
    ) -> list[Record]:
        query = """with active_keys as (
            select public from "jwk"."keys"
            where is_active = true
            order by
                case when is_primary = true then 0 else 1 end,
                created_at desc
            limit {limit} offset {offset}
        )
        select jsonb_build_object('keys', coalesce(jsonb_agg(public), '[]'::jsonb)) as jwks from active_keys
        """
        offset = page_size * (page - 1)
        return await connection.fetchval(query.format(limit=page_size, offset=offset))
