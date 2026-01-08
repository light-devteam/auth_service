from src.contexts.authentication.delivery.http.accounts.router import router
from src.contexts.authentication.delivery.http.accounts.create import router
from src.contexts.authentication.delivery.http.accounts.get import router
from src.contexts.authentication.delivery.http.accounts.get_identities import router
from src.contexts.authentication.delivery.http.accounts.get_identity_by_provider_id import router
from src.contexts.authentication.delivery.http.accounts.authenticate import router


__all__ = ['router']
