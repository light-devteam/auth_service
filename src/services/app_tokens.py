from uuid import UUID

from package import Token
from src.repositories import AppTokensRepository
from src.dto import AppTokenMetaDTO


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
