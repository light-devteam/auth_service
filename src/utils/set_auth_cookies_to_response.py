from datetime import datetime
from uuid import UUID

from fastapi import Response

from config import settings

def set_auth_cookie_to_response(
    response: Response,
    access_token: str,
    refresh_token: str,
    session_id: UUID,
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
        key='refresh_token',
        value=refresh_token,
        expires=expires_at,
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
        httponly=True,
    )
    response.set_cookie(
        key='session_id',
        value=session_id,
        expires=expires_at,
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
        httponly=True,
    )
    return Response
