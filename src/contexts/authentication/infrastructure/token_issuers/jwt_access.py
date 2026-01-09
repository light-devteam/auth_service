from datetime import datetime, timezone, timedelta

from dependency_injector.wiring import inject, Provide
import jwt

from src.contexts.authentication.domain.token_issuers import IAccessTokenIssuer
from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain.value_objects import AccessToken, ProviderConfig
from src.contexts.authentication.context import AuthenticationContext


class JWTAccessTokenIssuer(IAccessTokenIssuer):
    @inject
    def __init__(
        self,
        ctx: AuthenticationContext = Provide['auth.context'],
    ) -> None:
        self._ctx = ctx

    async def issue(
        self,
        issued_at: datetime,
        identity: Identity,
        provider_config: ProviderConfig,
    ) -> AccessToken:
        expires_at = issued_at + timedelta(minutes=provider_config.access_token_expire_minutes)
        token = jwt.encode(
            payload={
                'sub': str(identity.account_id),
                'iat': issued_at,
                'exp': expires_at,
            },
            headers={
                'kid': self._ctx.cache['jwks'][0]['private']['kid'],
            },
            key=jwt.PyJWK(self._ctx.cache['jwks'][0]['private']),
        )
        return AccessToken(
            token=token,
            issued_at=issued_at,
            expires_at=expires_at,
        )
