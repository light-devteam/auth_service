from uuid import UUID

from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.delivery.http.sessions.router import router
from src.contexts.authentication.application import ISessionService
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.patch('/revoke/{session_id}')
@inject
async def revoke(
    session_id: UUID,
    service: ISessionService = Depends(Provide['auth.session_service']),
    _: AuthContext = Depends(require_auth),
) -> None:
    await service.revoke(session_id)
