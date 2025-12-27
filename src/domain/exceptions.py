class AppException(Exception):
    _DETAIL: str = 'Oops, something went wrong'

    def __init__(self, detail: str | None = None, **kwargs):
        self.detail = detail or self._DETAIL
        self.extra = kwargs
        super().__init__(self.detail)


class DomainException(AppException):
    _DETAIL: str = 'Domain error occurred'


class ApplicationException(AppException):
    _DETAIL: str = 'Application error occurred'


class InfrastructureException(AppException):
    _DETAIL: str = 'Infrastructure error occurred'


class AccountNotFound(DomainException):
    _DETAIL: str = 'Account not found'
