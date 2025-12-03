from fastapi import Response, status, Depends, Cookie, HTTPException

from src.api.v1.session.router import router
from src.services import SessionsService
from src.dependencies import get_principal
from src.dto import PrincipalDTO
from src.schemas import RevokeOtherSessionsSchema
from src.enums import PrincipalTypes


@router.post('/revoke_other')
async def revoke_other(
    response: Response,
    token: PrincipalDTO = Depends(get_principal),
    revoke_data: RevokeOtherSessionsSchema | None = None,
    session_id: str | None = Cookie(default=None),
) -> None:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    account_id = token.id
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
