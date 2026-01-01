from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dependency_injector.wiring import inject, Provide

from src.domain import exceptions
from src.contexts.jwk.domain import exceptions as jwk_exceptions
from src.contexts.authentication.domain import exceptions as auth_exceptions
from src.infrastructure.logger import LoggerFactory

class ExceptionHandlersManager:
    @inject
    def __init__(
        self,
        app: FastAPI,
        logger_factory: LoggerFactory = Provide['logger_factory']
    ) -> None:
        self._app = app
        self._logger = logger_factory.get_logger(__name__)
        self._exception_to_handler = {
            exceptions.AppException: self.app_exception_handler,
            RequestValidationError: self.validation_exception_handler,
            Exception: self.general_exception_handler,
        }

    def register_exception_handlers(self) -> None:
        for exception, handler in self._exception_to_handler.items():
            self._app.add_exception_handler(exception, handler)
        self._logger.debug('All exception handlers registered')

    async def app_exception_handler(
        self,
        request: Request,
        exc: exceptions.AppException
    ) -> JSONResponse:
        status_code = self._map_exception_to_status(exc)
        self._logger.warning(
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
        self._logger.warning(
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
        self._logger.exception(
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
            auth_exceptions.IdentityForProviderAlreadyExists: status.HTTP_409_CONFLICT,
            auth_exceptions.IdentityAlreadyMain: status.HTTP_409_CONFLICT,
            auth_exceptions.IdentityNotFound: status.HTTP_404_NOT_FOUND,
            auth_exceptions.ProviderAlreadyExists: status.HTTP_409_CONFLICT,
            auth_exceptions.ProviderNotFound: status.HTTP_404_NOT_FOUND,
            auth_exceptions.ProviderNotActive: status.HTTP_403_FORBIDDEN,
            auth_exceptions.AccountNotFound: status.HTTP_404_NOT_FOUND,
            jwk_exceptions.JWKCannotDeactivatePrimary: status.HTTP_409_CONFLICT,
            jwk_exceptions.JWKAlreadyPrimary: status.HTTP_409_CONFLICT,
            jwk_exceptions.JWKAlreadyExists: status.HTTP_409_CONFLICT,
            jwk_exceptions.JWKNotFound: status.HTTP_404_NOT_FOUND,
            exceptions.ApplicationException: status.HTTP_500_INTERNAL_SERVER_ERROR,
            exceptions.DomainException: status.HTTP_400_BAD_REQUEST,
            exceptions.InfrastructureException: status.HTTP_503_SERVICE_UNAVAILABLE,
            exceptions.AppException: status.HTTP_503_SERVICE_UNAVAILABLE,
        }
        return mapping.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
