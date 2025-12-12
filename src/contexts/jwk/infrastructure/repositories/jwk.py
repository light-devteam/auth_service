from uuid import UUID

from dependency_injector.wiring import inject, Provide
from asyncpg import UniqueViolationError

from src.contexts.jwk.domain.repositories import IJWKRepository
from src.infrastructure.persistence.postgres import PostgresUnitOfWork
from src.contexts.jwk.domain import entities, value_objects, mappers, exceptions


class JWKRepository(IJWKRepository):
    _table_name = 'auth.jwks'

    @inject
    def __init__(
        self,
        mapper: mappers.JWKMapper = Provide['jwk_mapper'],
    ) -> None:
        self._mapper = mapper

    async def get_by_id(
        self,
        ctx: PostgresUnitOfWork,
        id: UUID | value_objects.JWKTokenID,
    ) -> entities.JWKToken:
        if isinstance(id, value_objects.JWKTokenID):
            id = id.value
        jwk_token = await ctx.connection.fetchrow(
            f'select * from {self._table_name} where id = $1',
            id,
        )
        if not jwk_token:
            raise exceptions.JWKNotFound()
        return self._mapper.to_entity(jwk_token)

    async def get_primary(self, ctx: PostgresUnitOfWork) -> entities.JWKToken:
        query = f'select * from {self._table_name} where is_primary = true'
        jwk_token = await ctx.connection.fetchrow(query)
        if not jwk_token:
            raise exceptions.JWKNotFound()
        return self._mapper.to_entity(jwk_token)

    async def get_all(
        self,
        ctx: PostgresUnitOfWork,
        page: int = 1,
        page_size: int = 100,
        only_active: bool = True,
    ) -> list[entities.JWKToken]:
        offset = (page - 1) * page_size
        where_clause = ''
        params = [offset, page_size]
        if only_active:
            where_clause = 'where is_active = $3'
            params.append(only_active)
        query = f"""
        select * from {self._table_name}
        {where_clause}
        order by is_primary desc, is_active desc, created_at desc
        offset $1 limit $2
        """
        raw_jwk_tokens = await ctx.connection.fetch(query, *params)
        jwk_tokens = []
        for raw_jwk_token in raw_jwk_tokens:
            jwk_tokens.append(self._mapper.to_entity(raw_jwk_token))
        return jwk_tokens

    async def create(
        self,
        ctx: PostgresUnitOfWork,
        jwk: entities.JWKToken,
    ) -> None:
        query = f"""
        insert into {self._table_name} (
            id,
            name,
            public,
            private,
            is_active,
            is_primary,
            created_at
        ) values ($1, $2, $3, $4, $5, $6, $7)
        """
        try:
            await ctx.connection.execute(
                query,
                jwk.id,
                jwk.name,
                str(jwk.public),
                jwk.private,
                jwk.is_active,
                jwk.is_primary,
                jwk.created_at,
            )
        except UniqueViolationError:
            raise exceptions.JWKAlreadyExists()

    async def update(
        self,
        ctx: PostgresUnitOfWork,
        *jwk_tokens: entities.JWKToken,
    ) -> None:
        if not jwk_tokens:
            return
        query = f"""
        update {self._table_name}
        set 
            name = $2,
            public = $3,
            private = $4,
            is_active = $5,
            is_primary = $6,
            created_at = $7
        where id = $1
        """
        values = [(
            jwk.id,
            jwk.name,
            str(jwk.public),
            jwk.private,
            jwk.is_active,
            jwk.is_primary,
            jwk.created_at,
        ) for jwk in jwk_tokens]
        try:
            await ctx.connection.executemany(query, values)
        except UniqueViolationError:
            raise exceptions.JWKAlreadyExists()

