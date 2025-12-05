# from fastapi import FastAPI, Request, status
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError

# from config import logger
# from src.shared.domain.exceptions import AuthBaseException


# def register_exception_handlers(app: FastAPI) -> None:
#     app.add_exception_handler(
#         AuthBaseException,
#         auth_exception_handler
#     )
#     app.add_exception_handler(
#         RequestValidationError,
#         validation_exception_handler
#     )
#     app.add_exception_handler(
#         Exception,
#         general_exception_handler
#     )
#     logger.debug('Exception handlers registered')


# async def auth_exception_handler(
#     request: Request,
#     exc: AuthBaseException
# ) -> JSONResponse:
#     logger.warning(
#         f'Auth exception: {exc.__class__.__name__} - {exc._DETAIL}',
#         extra={
#             'path': request.url.path,
#             'method': request.method,
#             'status_code': exc._STATUS_CODE,
#         }
#     )
#     return JSONResponse(
#         status_code=exc._STATUS_CODE,
#         content={
#             'detail': exc._DETAIL,
#             'error_type': exc.__class__.__name__,
#         }
#     )


# async def validation_exception_handler(
#     request: Request,
#     exc: RequestValidationError
# ) -> JSONResponse:
#     errors = exc.errors()
#     logger.warning(
#         f'Validation error on {request.url.path}',
#         extra={
#             'errors': errors,
#             'method': request.method,
#         }
#     )
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
#         content={
#             'detail': 'Validation error',
#             'errors': errors,
#         }
#     )


# async def general_exception_handler(
#     request: Request,
#     exc: Exception
# ) -> JSONResponse:
#     logger.exception(
#         f'Unexpected error: {str(exc)}',
#         extra={
#             'path': request.url.path,
#             'method': request.method,
#         }
#     )
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={
#             'detail': 'Internal server error',
#             'error_type': 'InternalServerError',
#         }
#     )
