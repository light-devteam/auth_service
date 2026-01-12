from asyncpg import UniqueViolationError
from dependency_injector.wiring import inject, Provide

from src.infrastructure.persistence.postgres import PostgresUnitOfWork
from src.contexts.authentication.domain import (
    value_objects,
    entities,
    repositories,
    mappers,
    exceptions,
)
from src.infrastructure.persistence.postgres import get_constraint_name


class RefreshTokenRepository(repositories.IRefreshTokenRepository):
    _table_name = 'auth.refresh_tokens'

    __one_active_token_on_one_session_uq_constraint = 'uq_refresh_tokens_session_active'

    @inject
    def __init__(
        self,
        mapper: mappers.RefreshTokenMapper = Provide['auth.refresh_token_mapper'],
    ) -> None:
        self._mapper = mapper

    async def create(
        self,
        ctx: PostgresUnitOfWork,
        refresh_token: entities.RefreshToken,
    ) -> None:
        query = f"""
        insert into {self._table_name} (
            id,
            session_id,
            hash,
            created_at,
            expires_at,
            revoked_at
        ) values ($1, $2, $3, $4, $5, $6)
        """
        try:
            await ctx.connection.execute(
                query,
                refresh_token.id,
                refresh_token.session_id,
                refresh_token.hash,
                refresh_token.created_at,
                refresh_token.expires_at,
                refresh_token.revoked_at,
            )
        except UniqueViolationError as exc:
            constraint_name = get_constraint_name(exc)
            match constraint_name:
                case self.__one_active_token_on_one_session_uq_constraint:
                    raise exceptions.ActiveRefreshTokenAlreadyExists()
                case _:
                    raise exceptions.InfrastructureException()

    async def get_by_id(
        self,
        ctx: PostgresUnitOfWork,
        id: value_objects.RefreshTokenID,
    ) -> entities.RefreshToken:
        refresh_token = await ctx.connection.fetchrow(
            f'select * from {self._table_name} where id = $1',
            id,
        )
        if not refresh_token:
            raise exceptions.RefreshTokenNotFound()
        return self._mapper.to_entity(refresh_token)

    async def get_by_session(
        self,
        ctx: PostgresUnitOfWork,
        session_id: value_objects.SessionID,
        page: int = 1,
        page_size: int = 10,
    ) -> list[entities.RefreshToken]:
        offset = (page - 1) * page_size
        query = f"""
        select * from {self._table_name}
        where session_id = $3
        order by created_at desc,
        offset $1 limit $2
        """
        raw_tokens = await ctx.connection.fetch(
            query,
            offset,
            page_size,
            session_id,
        )
        refresh_tokens = []
        for raw_token in raw_tokens:
            refresh_tokens.append(self._mapper.to_entity(raw_token))
        return refresh_tokens

    async def get_active_by_session(
        self,
        ctx: PostgresUnitOfWork,
        session_id: value_objects.SessionID,
    ) -> entities.RefreshToken:
        query = f"""
            select * from {self._table_name}
            where
                session_id = $1 and
                revoked_at is null
        """
        refresh_token = await ctx.connection.fetchrow(query, session_id)
        if not refresh_token:
            raise exceptions.RefreshTokenNotFound()
        return self._mapper.to_entity(refresh_token)

    async def update(
        self,
        ctx: PostgresUnitOfWork,
        *refresh_tokens: entities.RefreshToken,
    ) -> None:
        if not refresh_tokens:
            return
        query = f"""
        update {self._table_name}
        set 
            session_id = $2,
            hash = $3,
            created_at = $4,
            expires_at = $5,
            revoked_at = $6
        where id = $1
        """
        values = [(
            token.id,
            token.session_id,
            token.hash,
            token.created_at,
            token.expires_at,
            token.revoked_at,
        ) for token in refresh_tokens]
        try:
            await ctx.connection.executemany(query, values)
        except UniqueViolationError as exc:
            constraint_name = get_constraint_name(exc)
            match constraint_name:
                case self.__one_active_token_on_one_session_uq_constraint:
                    raise exceptions.ActiveRefreshTokenAlreadyExists()
                case _:
                    raise exceptions.InfrastructureException()
