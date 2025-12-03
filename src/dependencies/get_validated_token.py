from fastapi import Security
from fastapi.security import APIKeyCookie, HTTPAuthorizationCredentials, HTTPBearer

from src.services import SessionsService, AppTokensService
from src.exceptions import AccessTokenInvalid
from src.enums import TokenTypes
from src.dto import PrincipalDTO

cookie_security = APIKeyCookie(name='access_token', auto_error=False)
bearer_security = HTTPBearer(auto_error=False)


async def get_principal(
    cookie_token: str | None = Security(cookie_security),
    bearer_token: HTTPAuthorizationCredentials | None = Security(bearer_security),
) -> PrincipalDTO:
    token = None
    token_type = None
    if cookie_token:
        token = cookie_token
        token_type = TokenTypes.BEARER.value
    elif bearer_token:
        token = bearer_token.credentials
        token_type = bearer_token.scheme
    else:
        raise AccessTokenInvalid()
    if ':' in token:
        return await AppTokensService.validate(token_type, token)
    return await SessionsService.validate_access_token(token_type, token)
