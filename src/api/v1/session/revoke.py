from fastapi import Response, status, Cookie, HTTPException, Depends

from src.api.v1.session.router import router
from src.services import SessionsService
from src.schemas import RevokeSessionSchema
from src.utils import delete_auth_cookie
from src.dependencies import get_principal
from src.dto import PrincipalDTO
from src.enums import PrincipalTypes


@router.post('/revoke')
async def revoke(
    response: Response,
    token: PrincipalDTO = Depends(get_principal),
    revoke_data: RevokeSessionSchema | None = None,
    session_id: str | None = Cookie(default=None),
) -> None:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    account_id = token.id
    sid = session_id
    if revoke_data:
        account_id = revoke_data.account_id
        sid = revoke_data.session_id
    if not sid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='session_id is required',
        )
    await SessionsService.revoke(account_id, sid)
    if session_id == sid and token.id == account_id:
        response = delete_auth_cookie(response)
    response.status_code = status.HTTP_204_NO_CONTENT
