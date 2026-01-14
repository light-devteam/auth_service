from uuid import UUID

from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from msgspec import structs

from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.application import ISessionService
from src.contexts.authentication.delivery.http.accounts.schemas import Session
from src.delivery.dependencies import require_auth
from src.contexts.authentication.domain.value_objects import AuthContext


@router.get('/{account_id}/sessions')
@inject
async def get_sessions(
    account_id: UUID,
    page: int = 1,
    page_size: int = 100,
    service: ISessionService = Depends(Provide['auth.session_service']),
    _: AuthContext = Depends(require_auth),
) -> list[Session]:
    sessions = await service.get_by_account_id(account_id, page, page_size)
    return [Session(**structs.asdict(session)) for session in sessions]
