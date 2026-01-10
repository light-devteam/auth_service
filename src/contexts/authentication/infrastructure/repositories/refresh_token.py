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
