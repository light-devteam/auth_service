from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, APIKeyCookie, HTTPAuthorizationCredentials

from dependency_injector.wiring import inject, Provide

from src.contexts.authentication.application import IAuthService


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
) -> str:
    bearer_token = bearer.credentials if bearer is not None else ''
    token = bearer_token or cookie_token
    print(token, flush=True)
    await service.introspect(token)
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Not authenticateddddd",
    # )
