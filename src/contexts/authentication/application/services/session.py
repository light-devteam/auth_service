from uuid import UUID
from datetime import datetime, timezone

from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain import (
    value_objects,
    entities,
    repositories,
)
from src.domain.database_context import IDatabaseContext
from src.domain.value_objects import AccountID
from src.contexts.authentication.application.interfaces import ISessionService


class SessionApplicationService(ISessionService):
    @inject
    def __init__(
        self,
        session_repository: repositories.ISessionRepository = Provide['auth.session_repository'],
        provider_repository: repositories.IProviderRepository = Provide['auth.provider_repository'],
        refresh_token_repository: repositories.IRefreshTokenRepository = Provide['auth.refresh_token_repository'],
        database_context: IDatabaseContext = Provide['infrastructure.postgres_uow'],
    ) -> None:
        self._repository = session_repository
        self._provider_repository = provider_repository
        self._refresh_token_repository = refresh_token_repository
        self._db_ctx = database_context

    async def create(
        self,
        account_id: UUID,
        provider_type: value_objects.ProviderType,
    ) -> entities.Session:
        account_id = AccountID(account_id)
        async with self._db_ctx as ctx:
            await ctx.use_transaction()
            provider = await self._provider_repository.get_active_by_type(ctx, provider_type)
            session = entities.Session.create(
                account_id,
                provider.id,
            )
            await self._repository.create(ctx, session)
        return session

    async def get_by_id(self, id: UUID) -> entities.Session:
        id = value_objects.SessionID(id)
        async with self._db_ctx as ctx:
            return await self._repository.get_by_id(ctx, id)

    async def get_by_account_id(
        self,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[entities.Session]:
        account_id = AccountID(account_id)
        async with self._db_ctx as ctx:
            return await self._repository.get_by_account_id(
                ctx,
                account_id,
                page,
                page_size,
            )

    async def get_by_account_and_provider(
        self,
        account_id: UUID,
        provider_type: value_objects.ProviderType,
    ) -> entities.Session:
        account_id = AccountID(account_id)
        async with self._db_ctx as ctx:
            return await self._repository.get_by_account_and_provider(
                ctx,
                account_id,
                provider_type,
            )

    async def revoke(
        self,
        session_id: UUID,
    ) -> None:
        session_id = value_objects.SessionID(session_id)
        async with self._db_ctx as ctx:
            await ctx.use_transaction()
            session = await self._repository.get_by_id(ctx, session_id)
            refresh_token = await self._refresh_token_repository.get_active_by_session(
                ctx,
                session_id,
            )
            now = datetime.now(tz=timezone.utc)
            refresh_token.revoke(now)
            session.revoke(now)
            await self._refresh_token_repository.update(ctx, refresh_token)
            await self._repository.update(ctx, session)
