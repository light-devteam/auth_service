from fastapi import Security
from fastapi.security import APIKeyCookie, HTTPAuthorizationCredentials, HTTPBearer

from src.services import SessionsService
from src.exceptions import AccessTokenInvalid
from src.enums import TokenTypes
from src.dto import TokenPayloadDTO

cookie_security = APIKeyCookie(name='access_token', auto_error=False)
bearer_security = HTTPBearer(auto_error=False)


async def get_validated_token(
    cookie_token: str | None = Security(cookie_security),
    bearer_token: HTTPAuthorizationCredentials | None = Security(bearer_security),
) -> TokenPayloadDTO:
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
    return await SessionsService.validate_access_token(token_type, token)
