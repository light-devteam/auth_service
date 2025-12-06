from fastapi import status


class AppException(Exception):
    _STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAIL: str = 'Oops, something went wrong'

    def __init__(self, detail: str | None = None, **kwargs):
        self.detail = detail or self._DETAIL
        self.extra = kwargs
        super().__init__(self.detail)


class DomainException(AppException):
    _STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAIL: str = 'Domain error occurred'


class ApplicationException(AppException):
    _STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAIL: str = 'Application error occurred'


class InfrastructureException(AppException):
    _STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAIL: str = 'Infrastructure error occurred'
