from datetime import datetime, timezone, timedelta
import secrets

from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.domain.token_managers import IRefreshTokenManager
from src.contexts.authentication.domain.value_objects import RefreshToken, ProviderConfig
from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain.hashers import IHasher


class Base64RefreshTokenManager(IRefreshTokenManager):
    @inject
    def __init__(
        self,
        hasher: IHasher = Provide['auth.sha256_hasher']
    ) -> None:
        self._hasher = hasher
        self._prefix = 'b64'

    async def issue(
        self,
        issued_at: datetime,
        identity: Identity,
        provider_config: ProviderConfig,
    ) -> RefreshToken:
        if issued_at.tzinfo is None:
            issued_at = issued_at.replace(tzinfo=timezone.utc)
        token = secrets.token_urlsafe(32)
        hashed_token = self._hasher.hash(token.encode('utf-8'))
        return RefreshToken(
            token=token,
            prefix=self._prefix,
            hash=hashed_token,
            issued_at=issued_at,
            expires_at=issued_at + timedelta(days=provider_config.refresh_token_expire_days),
            account_id=identity.account_id,
        )

    @property
    def prefix(self) -> str:
        return self._prefix
