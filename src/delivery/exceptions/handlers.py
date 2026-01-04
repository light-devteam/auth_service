from typing import Type, Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dependency_injector.wiring import inject, Provide

from src.domain import exceptions
from src.delivery.exceptions.base_mapping_strategy import ExceptionMappingStrategy
from src.infrastructure.logger import LoggerFactory
from src.contexts.authentication.delivery.exceptions import AuthenticationExceptionMapping
from src.contexts.jwk.delivery.exceptions import JWKExceptionMapping


class ExceptionHandlersManager:
    @inject
    def __init__(
        self,
        app: FastAPI,
        strategies: list[ExceptionMappingStrategy] | None = None,
        logger_factory: LoggerFactory = Provide['infrastructure.logger_factory']
    ) -> None:
        self._app = app
        self._logger = logger_factory.get_logger(__name__)
        if strategies is None:
            strategies = [
                AuthenticationExceptionMapping(),
                JWKExceptionMapping(),
            ]
        self._exception_mapping = self._merge_strategies(strategies)
        self._logger.debug(f'{len(self._exception_mapping)} exception status codes registered')
        self._exception_to_handler = {
            exceptions.AppException: self.app_exception_handler,
            RequestValidationError: self.validation_exception_handler,
            Exception: self.general_exception_handler,
        }

    def register_exception_handlers(self) -> None:
        for exception, handler in self._exception_to_handler.items():
            self._app.add_exception_handler(exception, handler)
        self._logger.debug(f'{len(self._exception_to_handler)} exception handlers registered')

    async def app_exception_handler(
        self,
        request: Request,
        exc: exceptions.AppException
    ) -> JSONResponse:
        status_code = self._get_status_code(exc)
        self._logger.warning(
            f'App exception: {type(exc).__name__} - {exc.detail}',
            extra={
                'path': request.url.path,
                'method': request.method,
                'status_code': status_code,
            }
        )
        return JSONResponse(
            status_code=status_code,
            content={
                'detail': exc.detail,
                'error_type': type(exc).__name__,
            }
        )

    async def validation_exception_handler(
        self,
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:

        def clean_errors(errors: dict[str, Any]) -> list[str]:
            cleaned = []
            for e in errors:
                ctx = e.get('ctx', {})
                if isinstance(ctx.get('error'), Exception):
                    e['ctx'] = {'error': str(ctx['error'])}
                cleaned.append(e)
            return cleaned

        errors = clean_errors(exc.errors())
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

    def _merge_strategies(
        self,
        strategies: list[ExceptionMappingStrategy],
    ) -> dict[Type[exceptions.AppException], int]:
        combined = {
            exceptions.ApplicationException: status.HTTP_500_INTERNAL_SERVER_ERROR,
            exceptions.DomainException: status.HTTP_400_BAD_REQUEST,
            exceptions.InfrastructureException: status.HTTP_503_SERVICE_UNAVAILABLE,
            exceptions.AppException: status.HTTP_503_SERVICE_UNAVAILABLE,
        }
        for strategy in strategies:
            combined.update(strategy.get_mappings())
        return combined

    def _get_status_code(self, exc: exceptions.AppException) -> int:
        return self._exception_mapping.get(
            type(exc),
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
