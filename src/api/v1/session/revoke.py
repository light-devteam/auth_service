from fastapi import Response, status, Cookie, HTTPException

from src.api.v1.session.router import router
from src.services import SessionsService
from src.schemas import RevokeSessionSchema


@router.post('/revoke')
async def revoke(
    response: Response,
    revoke_data: RevokeSessionSchema | None = None,
    session_id: str | None = Cookie(default=None),
) -> None:
    sid = session_id or revoke_data.session_id
    if not sid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='session_id is required',
        )
    SessionsService.revoke(sid)
    response.status_code = status.HTTP_204_NO_CONTENT
