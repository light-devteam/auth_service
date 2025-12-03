from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import secrets
import base64

import jwt
from msgspec import structs
import bcrypt

from src import dto
from src.enums import TokenTypes
from config import settings


class Token:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 30

    @classmethod
    def create_pair(
        cls,
        subject: UUID | str,
        issued_at: datetime | None = None,
        **payload: dict,
    ) -> dto.TokenPairDTO:
        if not issued_at:
            issued_at = datetime.now(tz=timezone.utc)
        access = cls.create_access(
            subject=subject,
            issued_at=issued_at,
            **payload,
        )
        refresh = Token.create_refresh(issued_at=issued_at)
        return dto.TokenPairDTO(
            access=access,
            refresh=refresh,
            token_type=TokenTypes.BEARER,
        )

    @classmethod
    def create_access(
        cls,
        subject: UUID | str,
        issued_at: datetime | None = None,
        expires_at: datetime | None = None,
        **payload: dict,
    ) -> dto.AccessTokenDTO:
        if isinstance(subject, UUID):
            subject = str(subject)
        if not issued_at:
            issued_at = datetime.now(tz=timezone.utc)
        if not expires_at:
            expires_at = issued_at + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        jwt_token = jwt.encode(
            payload={
                'sub': subject,
                **payload,
                'iat': issued_at,
                'exp': expires_at,
            },
            headers={
                'kid': settings.JWK_PRIVATE_KEY.key_id,
            },
            key=settings.JWK_PRIVATE_KEY,
        )
        return dto.AccessTokenDTO(
            token=jwt_token,
            issued_at=issued_at,
            expires_at=expires_at,
        )

    @classmethod
    def create_refresh(
        cls,
        issued_at: datetime | None = None,
        expires_at: datetime | None = None,
    ) -> dto.RefreshTokenDTO:
        if not issued_at:
            issued_at = datetime.now(tz=timezone.utc)
        if not expires_at:
            expires_at = issued_at + timedelta(minutes=cls.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh = uuid4().hex
        return dto.RefreshTokenDTO(
            token=refresh,
            issued_at=issued_at,
            expires_at=expires_at,
            hash=Token.hash_sha256(refresh),
        )

    @classmethod
    def create_app(cls) -> dto.AppTokenDTO:
        token_bytes = secrets.token_bytes(32)
        token = base64.urlsafe_b64encode(token_bytes).decode()
        return dto.AppTokenDTO(token=token)

    @classmethod
    def decode_access(
        cls,
        token: str | bytes,
        options: dto.JwtDecodeOptionsDTO | None = None,
    ) -> dto.TokenPayloadDTO:
        if not options:
            options = dto.JwtDecodeOptionsDTO()
        key = ''
        if options.verify_signature:
            unverified_token = jwt.decode_complete(token, options={'verify_signature': False})
            key = settings.JWKS[unverified_token['header'].get('kid', '')]
        token_payload = jwt.decode(
            jwt=token,
            key=key,
            options=structs.asdict(options),
        )
        return dto.TokenPayloadDTO(**token_payload)

    @classmethod
    def hash_sha256(cls, token: str) -> str:
        return sha256(token.encode()).hexdigest()

    @classmethod
    def hash_bcrypt(cls, token: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(token.encode(), salt).decode()

    @classmethod
    def validate_bcrypt(cls, token: str, hashed_token: str) -> bool:
        return bcrypt.checkpw(token.encode(), hashed_token.encode())
