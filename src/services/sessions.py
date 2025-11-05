from uuid import UUID

from aiogram.utils.web_app import WebAppInitData
import jwt

from package import Token, Telegram
from src.dto import (
    DeviceInfoDTO,
    TokenPairDTO,
    TelegramAuthDataDTO,
    RedisTokenDataDTO,
    TokenPayloadDTO,
)
from src.exceptions import (
    AuthBaseException,
    AccessTokenInvalid,
    AccessTokenExpired,
    SessionDoesNotExistsException,
)
from src.repositories import SessionsRepository
from src.services.accounts import AccountsService
from src.enums import TokenTypes


class SessionsService:
    @classmethod
    async def create_session_from_init_data(
        cls,
        init_data: WebAppInitData,
        bot_name: str,
        device_info: DeviceInfoDTO,
    ) -> tuple[TokenPairDTO, UUID]:
        await Telegram.verify_init_data(init_data, bot_name)
        return await cls.__get_token(init_data.user.id, device_info)

    @classmethod
    async def create_session_from_auth_data(
        cls,
        auth_data: TelegramAuthDataDTO,
        device_info: DeviceInfoDTO,
    ) -> tuple[TokenPairDTO, UUID]:
        await Telegram.verify_auth_data(auth_data)
        return await cls.__get_token(auth_data.id, device_info)

    @classmethod
    async def __get_token(
        cls,
        telegram_id: int,
        device_info: DeviceInfoDTO,
    ) -> tuple[TokenPairDTO, UUID]:
        account = await AccountsService.get_account_from_telegram_id(telegram_id)
        try:
            token_pair = Token.create_pair(account.id)
        except Exception:
            raise AuthBaseException()
        session_id = await SessionsRepository.add_session(
            account_id=account.id,
            token_data=RedisTokenDataDTO(
                hash=token_pair.refresh.hash,
                ip=device_info.ip,
                issued_at=token_pair.refresh.issued_at,
                expires_at=token_pair.refresh.expires_at,
            ),
        )
        return token_pair, session_id

    @classmethod
    async def refresh_session(
        cls,
        session_id: UUID,
        refresh_token: str,
        device_info: DeviceInfoDTO,
    ) -> tuple[TokenPairDTO, UUID]:
        token_hash = Token.hash(refresh_token)
        session_data = await SessionsRepository.get_session(session_id)
        if session_data.token.hash != token_hash:
            raise SessionDoesNotExistsException()
        account_id = session_data.account_id
        try:
            token_pair = Token.create_pair(account_id)
        except Exception:
            raise AuthBaseException()
        new_session_id = await SessionsRepository.refresh_session(
            session_id=session_id,
            account_id=account_id,
            token_data=RedisTokenDataDTO(
                hash=token_pair.refresh.hash,
                ip=device_info.ip,
                issued_at=token_pair.refresh.issued_at,
                expires_at=token_pair.refresh.expires_at,
            ),
        )
        return token_pair, new_session_id

    @classmethod
    async def revoke(cls, account_id: UUID, session_id: UUID) -> None:
        return await SessionsRepository.revoke(account_id, session_id)

    @classmethod
    async def revoke_all(cls, account_id: UUID) -> None:
        return await SessionsRepository.revoke_all(account_id)

    @classmethod
    async def revoke_other(cls, account_id: UUID, keep_session_id: UUID) -> None:
        return await SessionsRepository.revoke_other(account_id, keep_session_id)

    @classmethod
    def check_access_type(cls, access_type: TokenTypes | str) -> None:
        if not access_type in TokenTypes:
            raise AccessTokenInvalid()

    @classmethod
    async def validate_access_token(
        cls,
        access_type: TokenTypes | str,
        token: str | bytes,
    ) -> TokenPayloadDTO:
        cls.check_access_type(access_type)
        try:
            return Token.decode_access(token)
        except jwt.ExpiredSignatureError:
            raise AccessTokenExpired()
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise AccessTokenInvalid()
