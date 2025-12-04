from uuid import UUID

from src.dto import AppDTO
from src.repositories import AppsRepository

class AppsService:
    @classmethod
    async def create_app(
        cls,
        account_id: UUID,
        name: str,
        description: str = '',
    ) -> UUID:
        return await AppsRepository.create_app(account_id, name, description)

    @classmethod
    async def get_apps(
        cls,
        account_id: UUID,
        page: int = 1,
        page_size: int = 100,
    ) -> list[AppDTO]:
        return await AppsRepository.get_apps(account_id, page, page_size)

    @classmethod
    async def get(
        cls,
        app_id: UUID,
    ) -> AppDTO:
        return await AppsRepository.get(app_id)

    @classmethod
    async def delete(cls, app_id: UUID) -> None:
        return await AppsRepository.delete(app_id)
