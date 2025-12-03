from fastapi import Response, status, Depends, HTTPException

from src.api.v1.session.router import router
from src.services import SessionsService
from src.dependencies import get_principal
from src.dto import PrincipalDTO
from src.utils import delete_auth_cookie
from src.schemas import RevokeAllSessionsSchema
from src.enums import PrincipalTypes


@router.post('/revoke_all')
async def revoke_all(
    response: Response,
    token: PrincipalDTO = Depends(get_principal),
    revoke_data: RevokeAllSessionsSchema | None = None
) -> None:
    if token.type == PrincipalTypes.APP:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    account_id = token.id
    if revoke_data:
        account_id = revoke_data.account_id
    await SessionsService.revoke_all(account_id)
    if account_id == token.id:
        response = delete_auth_cookie(response)
    response.status_code = status.HTTP_204_NO_CONTENT
