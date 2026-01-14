from fastapi import Depends, Response, Cookie
from dependency_injector.wiring import inject, Provide

import msgspec

from src.contexts.authentication.delivery.http.auth.router import router
from src.contexts.authentication.application import IAuthService
from src.contexts.authentication.delivery.http.auth.schemas import RefreshTokensRequest, TokenPair
from src.infrastructure.config import Settings


@router.post('/refresh')
@inject
async def refresh_tokens(
    response: Response,
    payload: RefreshTokensRequest | None = None,
    refresh_token: str = Cookie(''),
    service: IAuthService = Depends(Provide['auth.auth_service']),
    settings: Settings = Depends(Provide['infrastructure.settings']),
) -> TokenPair:
    if not refresh_token and payload is not None:
        refresh_token = payload.refresh_token
    access, refresh = await service.refresh(refresh_token)
    response.set_cookie(
        key='access_token',
        value=access.token,
        expires=access.expires_at,
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh.token,
        expires=refresh.expires_at,
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
        httponly=True,
    )
    return TokenPair(
        access=msgspec.structs.asdict(access),
        refresh=msgspec.structs.asdict(refresh),
    )
