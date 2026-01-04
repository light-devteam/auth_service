from typing import Any
from uuid import UUID

from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain import value_objects, entities, repositories
from src.domain.database_context import IDatabaseContext
from src.domain.value_objects import AccountID
from src.contexts.authentication.application.interfaces import ISessionService


class SessionApplicationService(ISessionService):
    @inject
    def __init__(
        self,
        repository: repositories.ISessionRepository = Provide['auth.session_repository'],
        database_context: IDatabaseContext = Provide['infrastructure.postgres_uow'],
    ) -> None:
        self._repository = repository
        self._db_ctx = database_context

    async def create(
        self,
        account_id: UUID,
        provider_id: UUID,
        credentials: dict[str, Any],
    ) -> entities.Session:
        account_id = AccountID(account_id)
        provider_id = value_objects.ProviderID(provider_id)
        session = entities.Session.create(
            account_id,
            provider_id,
        )
        async with self._db_ctx as ctx:
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

    async def get_by_account_id_and_provider_id(
        self,
        account_id: UUID,
        provider_id: UUID,
    ) -> entities.Session:
        account_id = AccountID(account_id)
        provider_id = value_objects.ProviderID(provider_id)
        async with self._db_ctx as ctx:
            return await self._repository.get_by_account_id_and_provider_id(
                ctx,
                account_id,
                provider_id,
            )
