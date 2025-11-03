from fastapi import status

class AccountsBaseException(Exception):
    _STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAIL = 'We are sorry, something went wrong'


class AuthDAOBaseException(AccountsBaseException): ...
class DeleteAllRowsException(AuthDAOBaseException): ...
class UpdateAllRowsException(AuthDAOBaseException): ...
