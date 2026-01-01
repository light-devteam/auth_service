from typing import Any
from uuid import UUID

from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain import value_objects, entities, repositories
from src.domain.database_context import IDatabaseContext
from src.domain.value_objects import AccountID
from src.contexts.authentication.application.interfaces import IIdentityService


class IdentityApplicationService(IIdentityService):
    @inject
    def __init__(
        self,
        repository: repositories.IIdentityRepository = Provide['auth.identity_repository'],
        database_context: IDatabaseContext = Provide['infrastructure.postgres_uow'],
    ) -> None:
        self._repository = repository
        self._db_ctx = database_context

    async def create(
        self,
        account_id: UUID,
        provider_id: UUID,
        provider_data: dict[str, Any],
    ) -> entities.Identity:
        account_id = AccountID(account_id)
        provider_id = value_objects.ProviderID(provider_id)
        identity = entities.Identity.create(
            account_id,
            provider_id,
            provider_data,
        )
        async with self._db_ctx as ctx:
            await self._repository.create(ctx, identity)
        return identity

    async def get_by_id(self, id: UUID) -> entities.Identity:
        id = value_objects.IdentityID(id)
        async with self._db_ctx as ctx:
            return await self._repository.get_by_id(ctx, id)

    async def get_by_account_id(
        self,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[entities.Identity]:
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
    ) -> entities.Identity:
        account_id = AccountID(account_id)
        provider_id = value_objects.ProviderID(provider_id)
        async with self._db_ctx as ctx:
            return await self._repository.get_by_account_id_and_provider_id(
                ctx,
                account_id,
                provider_id,
            )
