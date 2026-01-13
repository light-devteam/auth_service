from fastapi import Depends
from dependency_injector.wiring import inject, Provide

import msgspec

from src.contexts.authentication.delivery.http.auth.router import router
from src.contexts.authentication.application import IAuthService
from src.contexts.authentication.delivery.http.auth.schemas import GetToken, TokenPair


@router.post('/token')
@inject
async def get_token(
    payload: GetToken,
    service: IAuthService = Depends(Provide['auth.auth_service']),
) -> TokenPair:
    access, refresh = await service.get_token(
        payload.provider_type,
        payload.credentials,
    )
    return TokenPair(
        access=msgspec.structs.asdict(access),
        refresh=msgspec.structs.asdict(refresh),
    )
