from uuid import UUID

from package import Token
from src.repositories import AppTokensRepository
from src.dto import AppTokenMetaDTO
from src.enums import TokenTypes
from src.exceptions import AppTokenInvalidException
from src.dto import PrincipalDTO
from src.enums import PrincipalTypes


class AppTokensService:
    @classmethod
    async def create_token(
        cls,
        account_id: UUID,
        app_id: UUID,
        name: str,
    ) -> str:
        token_dto = Token.create_app()
        token_hash = Token.hash_bcrypt(token_dto.token)
        token_id = await AppTokensRepository.create_token(account_id, app_id, name, token_hash)
        return f'{token_id}:{token_dto.token}'

    @classmethod
    async def get_all(cls, account_id: UUID, app_id: UUID) -> list[AppTokenMetaDTO]:
        return await AppTokensRepository.get_all(account_id, app_id)

    @classmethod
    async def validate(cls, access_type: TokenTypes | str, app_token: str) -> PrincipalDTO:
        if isinstance(access_type, TokenTypes):
            access_type = access_type.value
        if access_type != TokenTypes.BEARER.value:
            raise AppTokenInvalidException()
        token_id, token = app_token.split(':')
        app_id, hashed_token = await AppTokensRepository.get_app_and_hash_by_id(token_id)
        if not Token.validate_bcrypt(token, hashed_token):
            raise AppTokenInvalidException()
        return PrincipalDTO(
            id=app_id,
            type=PrincipalTypes.APP,
        )
