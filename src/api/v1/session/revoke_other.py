from fastapi import Response, status, Depends, Cookie, HTTPException

from src.api.v1.session.router import router
from src.services import SessionsService
from src.dependencies import get_validated_token
from src.dto import TokenPayloadDTO
from src.schemas import RevokeOtherSessionsSchema


@router.post('/revoke_other')
async def revoke_other(
    response: Response,
    token: TokenPayloadDTO = Depends(get_validated_token),
    revoke_data: RevokeOtherSessionsSchema | None = None,
    session_id: str | None = Cookie(default=None),
) -> None:
    account_id = token.sub
    keep_sid = session_id
    if revoke_data:
        account_id = revoke_data.account_id
        keep_sid = revoke_data.keep_session_id
    if not keep_sid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='session ID is required',
        )
    await SessionsService.revoke_other(account_id, keep_sid)
    response.status_code = status.HTTP_204_NO_CONTENT
