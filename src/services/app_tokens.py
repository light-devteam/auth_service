from datetime import datetime
from uuid import UUID

from package import Token
from src.repositories import AppTokensRepository
from src.dto import AppTokenMetaDTO
from src.enums import TokenTypes
from src.exceptions import InvalidTokenException
from src.dto import PrincipalDTO
from src.enums import PrincipalTypes


class AppTokensService:
    @classmethod
    async def create_token(
        cls,
        app_id: UUID,
        name: str,
        expires_at: datetime | None = None,
    ) -> str:
        token_dto = Token.create_app()
        token_hash = Token.hash_bcrypt(token_dto.token)
        token_id = await AppTokensRepository.create_token(app_id, name, token_hash, expires_at)
        return f'{token_id}:{token_dto.token}'

    @classmethod
    async def get_all(
        cls,
        app_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[AppTokenMetaDTO]:
        return await AppTokensRepository.get_all(app_id, page,page_size)

    @classmethod
    async def get(
        cls,
        token_id: UUID,
    ) -> AppTokenMetaDTO:
        return await AppTokensRepository.get(token_id)

    @classmethod
    async def revoke(cls, token_id: UUID) -> None:
        return await AppTokensRepository.revoke(token_id)

    @classmethod
    async def validate(cls, access_type: TokenTypes | str, app_token: str) -> PrincipalDTO:
        if isinstance(access_type, TokenTypes):
            access_type = access_type.value
        if access_type != TokenTypes.BEARER.value:
            raise InvalidTokenException()
        token_id, token = app_token.split(':')
        validation_info = await AppTokensRepository.get_validation_info(token_id)
        if not Token.validate_bcrypt(token, validation_info.hash):
            raise InvalidTokenException()
        return PrincipalDTO(
            id=validation_info.app_id,
            type=PrincipalTypes.APP,
        )
