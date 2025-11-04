from fastapi import Request, Response, Cookie, status, HTTPException

from src.api.v1.session.router import router
from src.schemas import TokenPairSchema, RefreshSessionSchema
from src.services import SessionsService
from src.dto import DeviceInfoDTO
from src.utils import set_auth_cookie_to_response
from package import json_encoder

@router.post('/refresh')
async def refresh_session(
    request: Request,
    response: Response,
    refresh_data: RefreshSessionSchema | None = None,
    refresh_token_cookie: str | None = Cookie(default=None, alias='refresh_token'),
) -> TokenPairSchema:
    refresh_token = refresh_token_cookie or (refresh_data.refresh_token if refresh_data else None)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is missing',
        )
    device_info = DeviceInfoDTO(ip=request.state.ip)
    token_pair = await SessionsService.refresh_session(
        refresh_token=refresh_token,
        device_info=device_info,
    )
    set_auth_cookie_to_response(
        response,
        access_token=token_pair.access.token,
        token_type=token_pair.token_type,
        refresh_token=token_pair.refresh.token,
        expires_at=token_pair.refresh.expires_at,
    )
    return TokenPairSchema.model_validate_json(json_encoder.encode(token_pair))
