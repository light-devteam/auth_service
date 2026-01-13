from typing import Any
from datetime import datetime, timezone

from dependency_injector.wiring import inject, Provide

from src.domain import IDatabaseContext
from src.contexts.authentication.application.interfaces import IAuthService
from src.contexts.authentication.domain import (
    providers,
    repositories,
    value_objects,
    exceptions,
    entities,
)

class AuthApplicationService(IAuthService):
    @inject
    def __init__(
        self,
        database_context: IDatabaseContext = Provide['infrastructure.postgres_uow'],
        provider_registry: providers.IProviderFactory = Provide['auth_providers.registry'],
        session_repository: repositories.ISessionRepository = Provide['auth.session_repository'],
        provider_repository: repositories.IProviderRepository = Provide['auth.provider_repository'],
        identity_repository: repositories.IIdentityRepository = Provide['auth.identity_repository'],
        refresh_token_repository: repositories.IRefreshTokenRepository = Provide['auth.refresh_token_repository'],
    ) -> None:
        self._db_ctx = database_context
        self._provider_registry = provider_registry
        self._session_repository = session_repository
        self._provider_repository = provider_repository
        self._identity_repository = identity_repository
        self._refresh_token_repository = refresh_token_repository

    async def get_token(
        self,
        provider_type: value_objects.ProviderType,
        credentials: dict[str, Any],
    ) -> tuple[value_objects.AccessToken, value_objects.RefreshToken]:
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
            try:
                provider_entity = await self._provider_repository.get_active_by_type(
                    ctx,
                    provider_type,
                )
            except exceptions.ProviderNotFound:
                raise exceptions.InvalidCredentials()
            if identity.provider_id != provider_entity.id:

                # TODO: rotate identity if needed
                ...

            provider_config = provider.validate_config(provider_entity.config)
            now = datetime.now(tz=timezone.utc)
            access_token = await provider.access_token_manager.issue(
                issued_at=now,
                identity=identity,
                provider_config=provider_config,
            )
            refresh_token = await provider.refresh_token_manager.issue(
                issued_at=now,
                identity=identity,
                provider_config=provider_config,
            )
            session = entities.Session.create(
                identity.account_id,
                provider_entity.id,
            )
            refresh_token_entity = entities.RefreshToken.create(session.id, refresh_token)
            refresh_token.token = '{id}:{token}'.format(
                id=refresh_token_entity.id,
                token=refresh_token.token,
            )
            await self._session_repository.create(ctx, session)
            await self._refresh_token_repository.create(ctx, refresh_token_entity)
        return access_token, refresh_token
