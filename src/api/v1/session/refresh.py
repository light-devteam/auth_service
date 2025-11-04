from fastapi import Request, Response, Cookie, status, HTTPException

from src.api.v1.session.router import router
from src.schemas import TokenPairSchema, RefreshSessionSchema, SessionSchema
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
    session_id_cookie: str | None = Cookie(default=None, alias='session_id'),
) -> SessionSchema:
    refresh_token = refresh_token_cookie or (refresh_data.refresh_token if refresh_data else None)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is missing',
        )
    session_id = session_id_cookie or (refresh_data.session_id if refresh_data else None)
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Session ID is missing',
        )
    device_info = DeviceInfoDTO(ip=request.state.ip)
    token_pair, session_id = await SessionsService.refresh_session(
        session_id=session_id,
        refresh_token=refresh_token,
        device_info=device_info,
    )
    set_auth_cookie_to_response(
        response,
        access_token=token_pair.access.token,
        refresh_token=token_pair.refresh.token,
        session_id=session_id,
        expires_at=token_pair.refresh.expires_at,
    )
    token_pair_schema = TokenPairSchema.model_validate_json(json_encoder.encode(token_pair))
    return SessionSchema(
        session_id=session_id,
        token_pair=token_pair_schema,
    )
