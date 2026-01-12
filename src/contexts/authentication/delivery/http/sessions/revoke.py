from uuid import UUID

from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.delivery.http.sessions.router import router
from src.contexts.authentication.application import ISessionService


@router.patch('/revoke/{session_id}')
@inject
async def revoke(
    session_id: UUID,
    service: ISessionService = Depends(Provide['auth.session_service']),
) -> None:
    await service.revoke(session_id)
