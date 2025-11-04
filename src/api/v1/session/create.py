from typing import Union

from fastapi import Request, Response

from src.api.v1.session.router import router
from src.schemas import TelegramInitDataAuthSchema, TelegramAuthDataAuthSchema, TokenPairSchema
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
) -> TokenPairSchema:
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
    token_pair = await create_session_method
    set_auth_cookie_to_response(
        response,
        access_token=token_pair.access.token,
        token_type=token_pair.token_type,
        refresh_token=token_pair.refresh.token,
        expires_at=token_pair.refresh.expires_at,
    )
    return TokenPairSchema.model_validate_json(json_encoder.encode(token_pair))
