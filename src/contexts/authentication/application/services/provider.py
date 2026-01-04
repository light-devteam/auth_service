from typing import Any
from uuid import UUID

from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain.repositories import IProviderRepository
from src.contexts.authentication.domain.entities import Provider
from src.contexts.authentication.domain.value_objects import ProviderID, ProviderName, ProviderType
from src.domain import IDatabaseContext
from src.contexts.authentication.application.interfaces import IProviderService
from src.contexts.authentication.domain.services import ProviderService
from src.contexts.authentication.domain.exceptions import ProviderNotFound


class ProviderApplicationService(IProviderService):
    @inject
    def __init__(
        self,
        repository: IProviderRepository = Provide['auth.provider_repository'],
        database_context: IDatabaseContext = Provide['infrastructure.postgres_uow'],
        domain_service: ProviderService = Provide['auth.provider_domain_service']
    ) -> None:
        self._repository = repository
        self._db_ctx = database_context
        self._domain_service = domain_service

    async def create(
        self,
        name: str,
        type: str,
        config: dict[str, Any] | None = None,
    ) -> Provider:
        name = ProviderName(name)
        type = ProviderType(type)
        provider = Provider.create(name, type, config)
        async with self._db_ctx as ctx:
            await self._repository.create(ctx, provider)
        return provider

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 100,
        only_active: bool = True,
    ) -> list[Provider]:
        async with self._db_ctx as ctx:
            return await self._repository.get_all(ctx, page, page_size, only_active)

    async def get_by_id(self, id: UUID) -> Provider:
        id = ProviderID(id)
        async with self._db_ctx as ctx:
            return await self._repository.get_by_id(ctx, id)

    async def get_by_type(
        self,
        type: str,
        page: int = 1,
        page_size: int = 100,
    ) -> list[Provider]:
        type = ProviderType(type)
        async with self._db_ctx as ctx:
            return await self._repository.get_by_type(ctx, type, page, page_size)

    async def get_active_by_type(
        self,
        type: str,
    ) -> Provider:
        type = ProviderType(type)
        async with self._db_ctx as ctx:
            return await self._repository.get_active_by_type(ctx, type)

    async def activate(self, id: UUID) -> tuple[Provider, Provider | None]:
        id = ProviderID(id)
        async with self._db_ctx as ctx:
            await ctx.use_transaction()
            new_provider = await self._repository.get_by_id(ctx, id)
            try:
                old_provider = await self._repository.get_active_by_type(ctx, new_provider.type)
            except ProviderNotFound:
                old_provider = None
            new, old = self._domain_service.activate(new_provider, old_provider)
            await self._repository.update(ctx, old_provider, new_provider)
            return [new, old]
