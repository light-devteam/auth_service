from dependency_injector.wiring import inject, Provide

from src.domain.database_context import IDatabaseContext
from src.contexts.authentication.domain import (
    value_objects,
    entities,
    mappers,
    repositories,
    exceptions,
)
from src.domain.value_objects import AccountID


class SessionRepository(repositories.ISessionRepository):
    _table_name = 'auth.sessions'

    @inject
    def __init__(
        self,
        mapper: mappers.SessionMapper = Provide['auth.session_mapper'],
    ) -> None:
        self._mapper = mapper

    async def create(
        self,
        ctx: IDatabaseContext,
        session: entities.Session,
    ) -> None:
        query = f"""
        insert into {self._table_name} (
            id,
            account_id,
            provider_id,
            created_at,
            revoked_at
        ) values ($1, $2, $3, $4, $5)
        """
        await ctx.connection.execute(
            query,
            session.id,
            session.account_id,
            session.provider_id,
            session.created_at,
            session.revoked_at,
        )

    async def get_by_id(
        self,
        ctx: IDatabaseContext,
        id: value_objects.SessionID,
    ) -> entities.Session:
        session = await ctx.connection.fetchrow(
            f'select * from {self._table_name} where id = $1',
            id,
        )
        if not session:
            raise exceptions.SessionNotFound()
        return self._mapper.to_entity(session)

    async def get_by_account_id(
        self,
        ctx: IDatabaseContext,
        account_id: AccountID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[entities.Session]:
        offset = (page - 1) * page_size
        query = f"""
        select * from {self._table_name}
        where account_id = $3
        order by created_at desc
        offset $1 limit $2
        """
        raw_sessions = await ctx.connection.fetch(
            query,
            offset,
            page_size,
            account_id,
        )
        sessions = []
        for raw_session in raw_sessions:
            sessions.append(self._mapper.to_entity(raw_session))
        return sessions

    async def get_by_account_id_and_provider_id(
        self,
        ctx: IDatabaseContext,
        account_id: AccountID,
        provider_id: value_objects.ProviderID,
    ) -> entities.Session:
        query =f"""
        select * from {self._table_name}
        where
            account_id = $1 and
            provider_id = $2
        """
        session = await ctx.connection.fetchrow(
            query,
            account_id,
            provider_id,
        )
        if not session:
            raise exceptions.SessionNotFound()
        return self._mapper.to_entity(session)

    async def update(
        self,
        ctx: IDatabaseContext,
        *sessions: entities.Session,
    ) -> None:
        if not sessions:
            return
        query = f"""
        update {self._table_name}
        set 
            account_id = $2,
            provider_id = $3,
            created_at = $4,
            revoked_at = $5
        where id = $1
        """
        values = [(
            session.id,
            session.account_id,
            session.provider_id,
            session.created_at,
            session.revoked_at,
        ) for session in sessions]
        await ctx.connection.executemany(query, values)
