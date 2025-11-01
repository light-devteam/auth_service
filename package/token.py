from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from typing import Any
from hashlib import sha256

import jwt
from msgspec import structs

from src.dto import JwtDecodeOptionsDTO, AccessTokenDTO, RefreshTokenDTO, TokenPairDTO
from src.enums import TokenTypes
from config import settings


class Token:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 30

    @classmethod
    def create_pair(
        cls,
        subject: UUID,
        issued_at: datetime | None = None,
        **payload: dict,
    ) -> TokenPairDTO:
        if not issued_at:
            issued_at = datetime.now(tz=timezone.utc)
        access = cls.create_access(
            subject=subject,
            issued_at=issued_at,
            **payload,
        )
        refresh = Token.create_refresh(issued_at=issued_at)
        return TokenPairDTO(
            access=access,
            refresh=refresh,
            token_type=TokenTypes.BEARER,
        )

    @classmethod
    def create_access(
        cls,
        subject: UUID,
        key: str | dict | jwt.PyJWK,
        issued_at: datetime | None = None,
        expires_at: datetime | None = None,
        **payload: dict,
    ) -> str:
        if not issued_at:
            issued_at = datetime.now(tz=timezone.utc)
        if not expires_at:
            expires_at = issued_at + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        if isinstance(key, str):
            key = jwt.PyJWK.from_json(key)
        elif isinstance(key, dict):
            key = jwt.PyJWK.from_dict(key)
        jwt_token = jwt.encode(
            payload={
                'sub': subject,
                **payload,
                'iat': issued_at,
                'exp': expires_at,
            },
            key=key,
        )
        return AccessTokenDTO(
            token=jwt_token,
            issued_at=issued_at,
            expires_at=expires_at,
        )

    @classmethod
    def create_refresh(
        cls,
        issued_at: datetime | None = None,
        expires_at: datetime | None = None,
    ) -> None:
        if not issued_at:
            issued_at = datetime.now(tz=timezone.utc)
        if not expires_at:
            expires_at = issued_at + timedelta(minutes=cls.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh = uuid4().hex
        return RefreshTokenDTO(
            token=refresh,
            issued_at=issued_at,
            expires_at=expires_at,
            hash=Token.hash(refresh),
        )

    @classmethod
    def decode_access(
        cls,
        token: str | bytes,
        key: str | dict | jwt.PyJWK,
        options: JwtDecodeOptionsDTO | None = None,
    ) -> dict[str, Any]:
        if not options:
            options = JwtDecodeOptionsDTO()
        if isinstance(key, str):
            key = jwt.PyJWK.from_json(key)
        elif isinstance(key, dict):
            key = jwt.PyJWK.from_dict(key)
        return jwt.decode(
            jwt=token,
            key=key,
            options=structs.asdict(options),
        )

    @classmethod
    def hash(cls, token: str) -> str:
        return sha256(token.encode()).hexdigest()
