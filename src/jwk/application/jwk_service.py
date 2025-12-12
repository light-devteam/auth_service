from uuid import UUID

from dependency_injector.wiring import inject, Provide

from src.jwk.domain import repositories, entities, exceptions, services
from src.infrastructure.persistence.postgres import PostgresUnitOfWork


class JWKService:
    @inject
    def __init__(
        self,
        repository: repositories.IJWKRepository = Provide['jwk_repository'],
        database_context: PostgresUnitOfWork = Provide['postgres_uow'],
        domain_service: services.JWKTokenService = Provide['jwk_domain_service'],
    ) -> None:
        self._repository = repository
        self._db_ctx = database_context
        self._domain_service = domain_service

    async def get_by_id(self, id: UUID) -> entities.JWKToken:
        async with self._db_ctx as ctx:
            return await self._repository.get_by_id(ctx, id)

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 100,
        only_active: bool = True,
    ) -> list[entities.JWKToken]:
        async with self._db_ctx as ctx:
            return await self._repository.get_all(ctx, page, page_size, only_active)

    async def create(self, name: str) -> entities.JWKToken:
        token = entities.JWKToken.generate(name)
        async with self._db_ctx as ctx:
            await self._repository.create(ctx, token)
        return token

    async def toggle_active(self, id: UUID) -> entities.JWKToken:
        async with self._db_ctx as ctx:
            await ctx.use_transaction()
            token = await self._repository.get_by_id(ctx, id)
            token.toggle_active()
            await self._repository.update(ctx, token)
            return token

    async def set_primary(self, id: UUID) -> tuple[entities.JWKToken, entities.JWKToken]:
        async with self._db_ctx as ctx:
            await ctx.use_transaction()
            new_token = await self._repository.get_by_id(ctx, id)
            try:
                old_token = await self._repository.get_primary(ctx)
            except exceptions.JWKNotFound:
                old_token = None
            new_token, old_token = await self._domain_service.set_primary(new_token, old_token)
            if old_token:
                await self._repository.update(ctx, old_token, new_token)
            else:
                await self._repository.update(ctx, new_token)
            return new_token, old_token