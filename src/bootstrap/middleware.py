# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from config import settings, logger


# def register_middlewares(app: FastAPI) -> None:
#     _register_cors_middleware(app)
#     logger.debug('All middlewares registered')


# def _register_cors_middleware(app: FastAPI) -> None:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=settings.CORS_ALLOW_ORIGINS,
#         allow_credentials=True,
#         allow_methods=['*'],
#         allow_headers=['*'],
#     )
#     logger.debug(f'CORS middleware registered with origins: {settings.CORS_ALLOW_ORIGINS}')


# # def _register_ip_middleware(app: FastAPI) -> None:
# #     from src.middlewares import IPMiddleware
# #     app.add_middleware(IPMiddleware)
# #     logger.debug('IP middleware registered')


# # def _register_rate_limit_middleware(app: FastAPI) -> None:
# #     from package.rate_limiter import RateLimiter
# #     app.add_middleware(RateLimiter)
# #     logger.debug('Rate limit middleware registered')


# # def _register_request_id_middleware(app: FastAPI) -> None:
# #     from starlette_context import middleware
# #     app.add_middleware(middleware.RawContextMiddleware)
# #     logger.debug('Request ID middleware registered')
