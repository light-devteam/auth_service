from datetime import datetime, timezone, timedelta
import secrets

from src.contexts.authentication.domain.token_issuers import IRefreshTokenIssuer
from src.contexts.authentication.domain.value_objects import RefreshToken, ProviderConfig
from src.contexts.authentication.domain.entities import Identity


class Base64RefreshTokenIssuer(IRefreshTokenIssuer):
    async def issue(
        self,
        issued_at: datetime,
        identity: Identity,
        provider_config: ProviderConfig,
    ) -> RefreshToken:
        if issued_at.tzinfo is None:
            issued_at = issued_at.replace(tzinfo=timezone.utc)
        token = secrets.token_urlsafe(32)
        return RefreshToken(
            token=token,
            issued_at=issued_at,
            expires_at=issued_at + timedelta(days=provider_config.refresh_token_expire_days),
            account_id=identity.account_id,
        )