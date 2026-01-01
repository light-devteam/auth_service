from typing import Any

from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain.repositories import IProviderRepository
from src.contexts.authentication.domain.entities import Provider
from src.contexts.authentication.domain.value_objects import ProviderID, ProviderName
from src.domain import IDatabaseContext
from src.contexts.authentication.application.interfaces import IProviderService


class ProviderApplicationService(IProviderService):
    @inject
    def __init__(
        self,
        repository: IProviderRepository = Provide['auth.provider_repository'],
        database_context: IDatabaseContext = Provide['infrastructure.postgres_uow'],
    ) -> None:
        self._repository = repository
        self._db_ctx = database_context

    async def create(
        self,
        name: str,
        config: dict[str, Any] | None = None,
    ) -> Provider:
        name = ProviderName(name)
        provider = Provider.create(name, config)
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

    async def get_by_id(self, id: ProviderID) -> Provider:
        async with self._db_ctx as ctx:
            provider = await self._repository.get_by_id(ctx, id)
            return provider

    async def toggle_active(self, id: ProviderID) -> bool:
        async with self._db_ctx as ctx:
            await ctx.use_transaction()
            provider = await self._repository.get_by_id(ctx, id)
            current_state = provider.toggle_active()
            await self._repository.update(ctx, provider)
            return current_state
