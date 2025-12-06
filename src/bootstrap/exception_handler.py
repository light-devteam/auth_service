from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dependency_injector.wiring import inject, Provide

from src.shared.domain.exceptions import AppException
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
            AppException,
            self.auth_exception_handler
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

    async def auth_exception_handler(
        self,
        request: Request,
        exc: AppException
    ) -> JSONResponse:
        self.__logger.warning(
            f'Auth exception: {exc.__class__.__name__} - {exc._DETAIL}',
            extra={
                'path': request.url.path,
                'method': request.method,
                'status_code': exc._STATUS_CODE,
            }
        )
        return JSONResponse(
            status_code=exc._STATUS_CODE,
            content={
                'detail': exc._DETAIL,
                'error_type': exc.__class__.__name__,
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
