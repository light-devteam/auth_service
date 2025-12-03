from fastapi import status

class AuthBaseException(Exception):
    _STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAIL = 'We are sorry, something went wrong'


class BotNameIsNotSpecified(AuthBaseException):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DETAIL = 'Bot key most be specified'


class BotNameDoesNotExist(AuthBaseException):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DETAIL = 'The bot key does not exist'


class InvalidInitDataException(AuthBaseException):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DETAIL = 'Invalid telegram initData'


class AccountNotFoundException(AuthBaseException):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DETAIL = 'Account with id from telegram initData does not find'


class MaximumSessionsCreatedException(AuthBaseException):
    _STATUS_CODE = status.HTTP_403_FORBIDDEN
    _DETAIL = 'Account has maximum created sessions'


class AccessTokenExpired(AuthBaseException):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DETAIL = 'Recieved access token expired'


class AccessTokenInvalid(AuthBaseException):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DETAIL = 'Recieved access token invalid'


class SessionDoesNotExistsException(AuthBaseException):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DETAIL = 'Session with requested token hash does not exists'


class JWKBaseException(AuthBaseException): ...


class JWKNotFoundException(JWKBaseException):
    _STATUS_CODE = status.HTTP_404_NOT_FOUND
    _DETAIL = 'Requested JWK does not exists'


class JWKAlreadyExistsException(JWKBaseException):
    _STATUS_CODE = status.HTTP_409_CONFLICT
    _DETAIL = 'JWK with that name already exists'


class AppBaseException(AuthBaseException): ...


class AppAlreadyExistsException(AppBaseException):
    _STATUS_CODE = status.HTTP_409_CONFLICT
    _DETAIL = 'App with that name and account_id already exists'


class TokenAlreadyExistsException(AppBaseException):
    _STATUS_CODE = status.HTTP_409_CONFLICT
    _DETAIL = 'Token with that name and app_id already exists'


class AuthDAOBaseException(AuthBaseException): ...
class DeleteAllRowsException(AuthDAOBaseException): ...
class UpdateAllRowsException(AuthDAOBaseException): ...
