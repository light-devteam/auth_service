from typing import Any
from uuid import UUID

from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain import (
    value_objects,
    entities,
    repositories,
    providers,
    exceptions,
)
from src.domain.database_context import IDatabaseContext
from src.domain.value_objects import AccountID
from src.contexts.authentication.application.interfaces import ISessionService


class SessionApplicationService(ISessionService):
    @inject
    def __init__(
        self,
        repository: repositories.ISessionRepository = Provide['auth.session_repository'],
        provider_repository: repositories.IProviderRepository = Provide['auth.provider_repository'],
        identity_repository: repositories.IIdentityRepository = Provide['auth.identity_repository'],
        database_context: IDatabaseContext = Provide['infrastructure.postgres_uow'],
        provider_registry: providers.IProviderFactory = Provide['auth_providers.registry'],
    ) -> None:
        self._repository = repository
        self._provider_repository = provider_repository
        self._identity_repository = identity_repository
        self._db_ctx = database_context
        self._provider_registry = provider_registry

    async def authenticate(
        self,
        provider_type: value_objects.ProviderType,
        credentials: dict[str, Any],
    ) -> entities.Session:  # TODO: jwk pair, not Session
        provider = self._provider_registry.get(provider_type)
        input_credentials = provider.validate_credentials(credentials)
        async with self._db_ctx as ctx:
            await ctx.use_transaction()
            try:
                identity = await self._identity_repository.get_by_provider_and_login(
                    ctx,
                    provider_type,
                    provider.get_login_field(input_credentials),
                )
            except exceptions.IdentityNotFound:
                raise exceptions.InvalidCredentials()
            await provider.authenticate(input_credentials, identity.credentials)
            provider_entity = await self._provider_repository.get_active_by_type(
                ctx,
                provider_type,
            )
            # TODO: rotate if needed
            session = entities.Session.create(
                identity.account_id,
                provider_entity.id,
            )
            await self._repository.create(ctx, session)
        return session

    async def create(
        self,
        provider_type: value_objects.ProviderType,
        credentials: dict[str, Any],
    ) -> entities.Session:
        ...

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
