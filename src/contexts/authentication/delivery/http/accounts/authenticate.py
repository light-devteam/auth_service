from uuid import UUID

from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.application import ISessionService
from src.contexts.authentication.delivery.http.accounts.schemas import AuthenticateRequest


@router.post('/authenticate')
@inject
async def authenticate(
    payload: AuthenticateRequest,
    service: ISessionService = Depends(Provide['auth.session_service']),
) -> UUID:
    session = await service.authenticate(
        payload.provider_type,
        payload.credentials,
    )
    return session.id
