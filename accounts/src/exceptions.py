from fastapi import status

class AccountsBaseException(Exception):
    _STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAIL = 'We are sorry, something went wrong'


class AccountNotFoundException(AccountsBaseException):
    _STATUS_CODE = status.HTTP_404_NOT_FOUND
    _DETAIL = 'Account not found'


class AccountAlreadyExistsException(AccountsBaseException):
    _STATUS_CODE = status.HTTP_409_CONFLICT
    _DETAIL = 'Account already exists'


class AuthDAOBaseException(AccountsBaseException): ...
class DeleteAllRowsException(AuthDAOBaseException): ...
class UpdateAllRowsException(AuthDAOBaseException): ...
