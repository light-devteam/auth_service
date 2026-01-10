from fastapi import Depends
from dependency_injector.wiring import inject, Provide

import msgspec

from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.application import IAccountService
from src.contexts.authentication.delivery.http.accounts.schemas import AuthenticateRequest, TokenPair


@router.post('/authenticate')
@inject
async def authenticate(
    payload: AuthenticateRequest,
    service: IAccountService = Depends(Provide['auth.accounts_service']),
) -> TokenPair:
    access, refresh = await service.authenticate(
        payload.provider_type,
        payload.credentials,
    )
    return TokenPair(
        access=msgspec.structs.asdict(access),
        refresh=msgspec.structs.asdict(refresh),
    )
