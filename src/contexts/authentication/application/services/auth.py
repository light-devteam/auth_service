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
    token_managers,
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
        access_token_jwt_manager: token_managers.IAccessTokenManager = Provide['auth.access_token_jwt_manager'],
    ) -> None:
        self._db_ctx = database_context
        self._provider_registry = provider_registry
        self._session_repository = session_repository
        self._provider_repository = provider_repository
        self._identity_repository = identity_repository
        self._refresh_token_repository = refresh_token_repository
        self._access_token_jwt_manager = access_token_jwt_manager

    async def get_token(
        self,
        provider_type: value_objects.ProviderType,
        credentials: dict[str, Any],
    ) -> tuple[value_objects.Token, value_objects.Token]:
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
            identity.update_last_used(now)
            await self._identity_repository.update(ctx, identity)
            await self._refresh_token_repository.create(ctx, refresh_token_entity)
        return access_token, refresh_token

    async def refresh(
        self,
        refresh_token: str,
    ) -> tuple[value_objects.Token, value_objects.Token]:
        id, token = refresh_token.split(':', maxsplit=1)
        id = value_objects.RefreshTokenID(id)
        async with self._db_ctx as ctx:
            await ctx.use_transaction()
            old_refresh_token = await self._refresh_token_repository.get_by_id(ctx, id)
            session = await self._session_repository.get_by_id(ctx, old_refresh_token.session_id)
            provider_entity = await self._provider_repository.get_by_id(ctx, session.provider_id)
            provider = self._provider_registry.get(provider_entity.type)
            await provider.refresh_token_manager.validate(token, old_refresh_token.hash)
            identity = await self._identity_repository.get_by_account_and_provider(
                ctx,
                session.account_id,
                provider_entity.type,
            )
            provider_config = provider.validate_config(provider_entity.config)
            now = datetime.now(tz=timezone.utc)
            new_access_token = await provider.access_token_manager.issue(
                issued_at=now,
                identity=identity,
                provider_config=provider_config,
            )
            new_refresh_token = await provider.refresh_token_manager.issue(
                issued_at=now,
                identity=identity,
                provider_config=provider_config,
            )
            new_refresh_token_entity = entities.RefreshToken.create(session.id, new_refresh_token)
            new_refresh_token.token = '{id}:{token}'.format(
                id=new_refresh_token_entity.id,
                token=new_refresh_token.token,
            )
            try:
                old_refresh_token.revoke(now)
            except exceptions.TokenAlreadyRevoked:
                raise exceptions.InvalidToken('Refresh token invalid')
            await self._refresh_token_repository.update(ctx, old_refresh_token)
            await self._refresh_token_repository.create(ctx, new_refresh_token_entity)
        return new_access_token, new_refresh_token

    async def introspect(
        self,
        access_token: str,
    ) -> None:
        token_type = self.__get_token_type(access_token)
        if token_type == 'jwt':
            return await self._access_token_jwt_manager.validate(access_token)
        raise exceptions.InvalidToken('Access token invalid')

    def __get_token_type(self, token: str) -> str:
        if len(token.split(':')) > 1:
            return 'opaque'
        return 'jwt'
