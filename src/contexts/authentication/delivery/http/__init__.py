from src.contexts.authentication.delivery.http.accounts import router as accounts_router
from src.contexts.authentication.delivery.http.providers import router as providers_router


__all__ = [
    'accounts_router',
    'providers_router',
]
