from fastapi import Depends, Response
from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.delivery.http.sessions.router import router
from src.contexts.authentication.application import ISessionService
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext
from src.infrastructure.config import Settings


@router.patch('/revoke')
@inject
async def revoke_self(
    response: Response,
    service: ISessionService = Depends(Provide['auth.session_service']),
    settings: Settings = Depends(Provide['infrastructure.settings']),
    auth: AuthContext = Depends(require_auth),
) -> Response:
    await service.revoke(auth.session_id)
    response.delete_cookie(
        key='access_token',
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
    )
    response.delete_cookie(
        key='refresh_token',
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
        httponly=True,
    )
