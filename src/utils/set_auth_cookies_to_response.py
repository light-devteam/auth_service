from datetime import datetime

from fastapi import Response

from config import settings
from src.enums import TokenTypes

def set_auth_cookie_to_response(
    response: Response,
    access_token: str,
    token_type: TokenTypes,
    refresh_token: str,
    expires_at: datetime,
) -> Response:
    response.set_cookie(
        key='access_token',
        value=access_token,
        expires=expires_at,
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
    )
    response.set_cookie(
        key='token_type',
        value=token_type.value,
        expires=expires_at,
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        expires=expires_at,
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
        httponly=True,
    )
    return Response
