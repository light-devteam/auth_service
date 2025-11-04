from uuid import UUID

import httpx
from fastapi import status

from src.exceptions import AuthBaseException, AccountNotFoundException
from config import settings
from src.dto import AccountDTO

class AccountsService:
    GET_ACCOUNT_FROM_TG_ID_URL = '{domain}/api/v1/accounts/telegram/{telegram_id}'

    @classmethod
    async def get_account_from_telegram_id(cls, telegram_id: int) -> AccountDTO:
        url = cls.GET_ACCOUNT_FROM_TG_ID_URL.format(
            domain=settings.ACCOUNTS_SERVICE_URL,
            telegram_id=telegram_id,
        )
        async with httpx.AsyncClient(http2=True) as client:
            try:
                account_data = await client.get(url)
            except httpx.HTTPError:
                raise AuthBaseException()
            if account_data.status_code == status.HTTP_404_NOT_FOUND:
                raise AccountNotFoundException()
        try:
            return AccountDTO(id=UUID(account_data.json()['id']))
        except Exception:
            raise AuthBaseException()
