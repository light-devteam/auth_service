from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dependency_injector.wiring import inject, Provide

from src.shared.domain import exceptions
from src.shared.infrastructure.logger import LoggerFactory

class ExceptionHandler:
    @inject
    def __init__(
        self,
        app: FastAPI,
        logger_factory: LoggerFactory = Provide['logger_factory']
    ) -> None:
        self.__logger = logger_factory.get_logger(__name__)
        app.add_exception_handler(
            exceptions.AppException,
            self.app_exception_handler
        )
        app.add_exception_handler(
            RequestValidationError,
            self.validation_exception_handler
        )
        app.add_exception_handler(
            Exception,
            self.general_exception_handler
        )
        self.__logger.debug('Exception handlers registered')

    async def app_exception_handler(
        self,
        request: Request,
        exc: exceptions.AppException
    ) -> JSONResponse:
        status_code = self._map_exception_to_status(exc)
        self.__logger.warning(
            f'App exception: {type(exc).__name__} - {exc._DETAIL}',
            extra={
                'path': request.url.path,
                'method': request.method,
                'status_code': status_code,
            }
        )
        return JSONResponse(
            status_code=status_code,
            content={
                'detail': exc._DETAIL,
                'error_type': type(exc).__name__,
            }
        )

    async def validation_exception_handler(
        self,
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
        errors = exc.errors()
        self.__logger.warning(
            f'Validation error on {request.url.path}',
            extra={
                'errors': errors,
                'method': request.method,
            }
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                'detail': 'Validation error',
                'errors': errors,
            }
        )

    async def general_exception_handler(
        self,
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        self.__logger.exception(
            f'Unexpected error: {str(exc)}',
            extra={
                'path': request.url.path,
                'method': request.method,
            }
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'detail': 'Internal server error',
                'error_type': 'InternalServerError',
            }
        )

    def _map_exception_to_status(self, exc: exceptions.AppException) -> int:
        mapping = {
            exceptions.ApplicationException: status.HTTP_500_INTERNAL_SERVER_ERROR,
            exceptions.DomainException: status.HTTP_400_BAD_REQUEST,
            exceptions.InfrastructureException: status.HTTP_503_SERVICE_UNAVAILABLE,
            exceptions.AppException: status.HTTP_503_SERVICE_UNAVAILABLE,
        }
        return mapping.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
