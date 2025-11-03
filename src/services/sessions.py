from aiogram.utils.web_app import WebAppInitData

from package import Token, Telegram
from src.dto import DeviceInfoDTO, TokenPairDTO, TelegramAuthDataDTO
from src.exceptions import AuthBaseException
from src.repositories import SessionsRepository
from src.services.accounts import AccountsService


class SessionsService:
    @classmethod
    async def create_session_from_init_data(
        cls,
        init_data: WebAppInitData,
        bot_name: str,
        device_info: DeviceInfoDTO,
    ) -> TokenPairDTO:
        await Telegram.verify_init_data(init_data, bot_name)
        return await cls.__get_token(init_data.user.id, device_info)

    @classmethod
    async def create_session_from_auth_data(
        cls,
        auth_data: TelegramAuthDataDTO,
        device_info: DeviceInfoDTO,
    ) -> TokenPairDTO:
        await Telegram.verify_auth_data(auth_data)
        return await cls.__get_token(auth_data.id, device_info)

    @classmethod
    async def __get_token(
        cls,
        telegram_id: int,
        device_info: DeviceInfoDTO,
    ) -> TokenPairDTO:
        account = await AccountsService.get_account_from_telegram_id(telegram_id)
        try:
            token_pair = Token.create_pair(account.id)
        except Exception as exception:
            raise AuthBaseException()
        await SessionsRepository.add_session(
            account_id=account.id,
            token_hash=token_pair.refresh.hash,
            device_info=device_info,
            expires_at=token_pair.refresh.expires_at,
            issued_at=token_pair.refresh.issued_at,
        )
        return token_pair