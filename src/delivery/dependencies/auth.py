from fastapi import Depends, Request
from fastapi.security import HTTPBearer, APIKeyCookie, HTTPAuthorizationCredentials

from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.application import IAuthService
from src.contexts.authentication.domain.value_objects import AuthContext


bearer_scheme = HTTPBearer(
    scheme_name='BearerAuth',
    description='Bearer token in Authorization header',
    auto_error=False,
)

cookie_scheme = APIKeyCookie(
    name='access_token',
    scheme_name='CookieAuth',
    description='Access token in cookie',
    auto_error=False,
)


@inject
async def require_auth(
    request: Request,
    bearer: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    cookie_token: str = Depends(cookie_scheme),
    service: IAuthService = Depends(Provide['auth.auth_service']),
) -> AuthContext:
    bearer_token = bearer.credentials if bearer is not None else ''
    token = cookie_token or bearer_token
    return await service.introspect(token)
