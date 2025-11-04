from typing import Union

from fastapi import Request, Response

from src.api.v1.session.router import router
from src.schemas import (
    TelegramInitDataAuthSchema,
    TelegramAuthDataAuthSchema,
    TokenPairSchema,
    SessionSchema,
)
from src.services import SessionsService
from src.dto import DeviceInfoDTO, TelegramAuthDataDTO
from src.utils import set_auth_cookie_to_response
from package import json_encoder


@router.post('')
async def auth(
    request: Request,
    auth_data: Union[
        TelegramInitDataAuthSchema,
        TelegramAuthDataAuthSchema,
    ],
    response: Response,
) -> SessionSchema:
    device_info = DeviceInfoDTO(ip=request.state.ip)
    if isinstance(auth_data, TelegramInitDataAuthSchema):
        create_session_method = SessionsService.create_session_from_init_data(
            auth_data.telegram_init_data,
            auth_data.bot_name,
            device_info,
        )
    else:
        create_session_method = SessionsService.create_session_from_auth_data(
            TelegramAuthDataDTO(**auth_data.telegram_auth_data.model_dump()),
            device_info,
        )
    token_pair, session_id = await create_session_method
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
