from uuid import UUID

from src.dto import AppDTO
from src.enums import AppTypes
from src.repositories import AppsRepository

class AppsService:
    @classmethod
    async def create_app(
        cls,
        account_id: UUID,
        name: str,
        type: AppTypes,
        description: str = '',
    ) -> UUID:
        return await AppsRepository.create_app(account_id, name, type, description)

    @classmethod
    async def get_apps(
        cls,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[AppDTO]:
        return await AppsRepository.get_apps(account_id, page, page_size)
