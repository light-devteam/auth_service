from src.domain.exceptions import DomainException


class ProviderNotActive(DomainException):
    _DETAIL = 'Provider not active'


class ProviderNotFound(DomainException):
    _DETAIL = 'Provider not found'


class ProviderAlreadyExists(DomainException):
    _DETAIL = 'Provider with that name already exists'


class IdentityForProviderAlreadyExists(DomainException):
    _DETAIL = 'Identity for this provider already exists'


class SessionAlreadyRevoked(DomainException):
    _DETAIL = 'Account session already has been revoked'


class TokenAlreadyRevoked(DomainException):
    _DETAIL = 'Session refresh token already has been revoked'


class AccountNotFound(DomainException):
    _DETAIL: str = 'Account not found'


class IdentityNotFound(DomainException):
    _DETAIL: str = 'Account identity not found'
