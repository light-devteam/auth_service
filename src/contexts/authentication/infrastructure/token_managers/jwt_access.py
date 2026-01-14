from uuid import UUID
from datetime import datetime, timezone, timedelta

from dependency_injector.wiring import inject, Provide
import jwt

from src.contexts.authentication.domain.token_managers import IAccessTokenManager
from src.contexts.authentication.domain.entities import Identity
from src.contexts.authentication.domain import value_objects
from src.contexts.authentication.context import AuthenticationContext
from src.contexts.authentication.domain.exceptions import InvalidToken


class JWTAccessTokenManager(IAccessTokenManager):
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
        provider_config: value_objects.ProviderConfig,
        session_id: value_objects.SessionID,
    ) -> value_objects.JWTToken:
        if issued_at.tzinfo is None:
            issued_at = issued_at.replace(tzinfo=timezone.utc)
        expires_at = issued_at + timedelta(minutes=provider_config.access_token_expire_minutes)
        token = jwt.encode(
            payload={
                'sub': str(identity.account_id),
                'sid': str(session_id),
                'iat': issued_at,
                'exp': expires_at,
            },
            headers={
                'kid': self._ctx.cache['private_jwks'].keys[0].key_id,
            },
            key=self._ctx.cache['private_jwks'].keys[0],
        )
        return value_objects.JWTToken(
            token=token,
            issued_at=issued_at,
            expires_at=expires_at,
        )

    async def validate(
        self,
        token: str,
    ) -> value_objects.AuthContext:
        try:
            header = jwt.get_unverified_header(token)
        except jwt.PyJWTError:
            raise InvalidToken('Access token invalid')
        try:
            decoded_token = jwt.decode_complete(
                token,
                key=self._ctx.cache['public_jwks'][header['kid']],
                options={
                    'verify_signature': True,
                    'verify_exp': True,
                    # 'verify_nbf': True,
                    'verify_iat': True,
                    # 'verify_aud': True,
                    # 'verify_iss': True,
                    'verify_sub': True,
                    # 'verify_jti': True,
                }
            )
        except jwt.PyJWTError:
            raise InvalidToken('Access token invalid')
        return value_objects.AuthContext(
            account_id=UUID(decoded_token['payload']['sub']),
            session_id=UUID(decoded_token['payload']['sid']),
        )
