from fastapi import Depends
from dependency_injector.wiring import inject, Provide

import msgspec

from src.contexts.authentication.delivery.http.auth.router import router
from src.contexts.authentication.application import IAuthService
from src.contexts.authentication.delivery.http.auth.schemas import RefreshTokensRequest, TokenPair


@router.post('/refresh')
@inject
async def refresh_tokens(
    payload: RefreshTokensRequest,
    service: IAuthService = Depends(Provide['auth.auth_service']),
) -> TokenPair:
    access, refresh = await service.refresh(payload.refresh_token)
    return TokenPair(
        access=msgspec.structs.asdict(access),
        refresh=msgspec.structs.asdict(refresh),
    )
