from fastapi import Depends, Response
from dependency_injector.wiring import inject, Provide

import msgspec

from src.contexts.authentication.delivery.http.auth.router import router
from src.contexts.authentication.application import IAuthService
from src.contexts.authentication.delivery.http.auth.schemas import GetToken, TokenPair
from src.infrastructure.config import Settings


@router.post('/token')
@inject
async def get_token(
    response: Response,
    payload: GetToken,
    service: IAuthService = Depends(Provide['auth.auth_service']),
    settings: Settings = Depends(Provide['infrastructure.settings']),
) -> TokenPair:
    access, refresh = await service.get_token(
        payload.provider_type,
        payload.credentials,
    )
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
