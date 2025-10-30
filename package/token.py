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
    @staticmethod
    def create_pair(
        subject: UUID,
        issued_at: datetime | None = None,
        **payload: dict,
    ) -> TokenPairDTO:
        if not issued_at:
            issued_at = datetime.now(tz=timezone.utc)
        access = Token.create_access(
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

    @staticmethod
    def create_access(
        subject: UUID,
        issued_at: datetime | None = None,
        expires_at: datetime | None = None,
        **payload: dict,
    ) -> str:
        if not issued_at:
            issued_at = datetime.now(tz=timezone.utc)
        if not expires_at:
            expires_at = issued_at + timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MINUTES)
        jwt_token = jwt.encode(
            payload={
                'sub': subject,
                **payload,
                'iat': issued_at,
                'exp': expires_at,
            },
            key=settings.JWT_PRIVATE_KEY,
            algorithm=settings.JWT_ALGORITHM.value,
        )
        return AccessTokenDTO(
            token=jwt_token,
            issued_at=issued_at,
            expires_at=expires_at,
        )

    @staticmethod
    def create_refresh(
        issued_at: datetime | None = None,
        expires_at: datetime | None = None,
    ) -> None:
        if not issued_at:
            issued_at = datetime.now(tz=timezone.utc)
        if not expires_at:
            expires_at = issued_at + timedelta(minutes=settings.JWT_REFRESH_EXPIRE_DAYS)
        refresh = uuid4().hex
        return RefreshTokenDTO(
            token=refresh,
            issued_at=issued_at,
            expires_at=expires_at,
            hash=Token.hash(refresh),
        )

    @staticmethod
    def decode_access(
        token: str | bytes,
        options: JwtDecodeOptionsDTO | None = None,
    ) -> dict[str, Any]:
        if not options:
            options = JwtDecodeOptionsDTO()
        return jwt.decode(
            jwt=token,
            key=settings.JWT_PUBLIC_KEY,
            algorithms=[settings.JWT_ALGORITHM.value],
            options=structs.asdict(options),
        )

    @staticmethod
    def hash(token: str) -> str:
        return sha256(token.encode()).hexdigest()
