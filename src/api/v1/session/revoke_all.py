from fastapi import Response, status, Depends

from src.api.v1.session.router import router
from src.services import SessionsService
from src.dependencies import get_validated_token
from src.dto import TokenPayloadDTO
from src.utils import delete_auth_cookie
from src.schemas import RevokeAllSessionsSchema


@router.post('/revoke_all')
async def revoke_all(
    response: Response,
    token: TokenPayloadDTO = Depends(get_validated_token),
    revoke_data: RevokeAllSessionsSchema | None = None
) -> None:
    account_id = token.sub
    if revoke_data:
        account_id = revoke_data.account_id
    await SessionsService.revoke_all(account_id)
    if account_id == token.sub:
        response = delete_auth_cookie(response)
    response.status_code = status.HTTP_204_NO_CONTENT
