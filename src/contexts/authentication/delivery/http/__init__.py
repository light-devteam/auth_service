from src.contexts.authentication.delivery.http.accounts import router as accounts_router
from src.contexts.authentication.delivery.http.providers import router as providers_router
from src.contexts.authentication.delivery.http.identities import router as identities_router
from src.contexts.authentication.delivery.http.sessions import router as sessions_router
from src.contexts.authentication.delivery.http.auth import router as auth_router


__all__ = [
    'accounts_router',
    'providers_router',
    'identities_router',
    'sessions_router',
    'auth_router',
]
