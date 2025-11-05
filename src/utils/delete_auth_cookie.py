from fastapi import Response

from config import settings

def delete_auth_cookie(response: Response) -> Response:
    response.delete_cookie(
        key='access_token',
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
    )
    response.delete_cookie(
        key='refresh_token',
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
        httponly=True,
    )
    response.delete_cookie(
        key='session_id',
        domain=settings.COOKIE_DOMAIN,
        secure=True,
        samesite='lax',
        httponly=True,
    )
    return Response
