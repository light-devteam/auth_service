from src.domain.exceptions import DomainException, InfrastructureException


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
    _DETAIL = 'Account not found'


class IdentityNotFound(DomainException):
    _DETAIL = 'Account identity not found'


class SessionNotFound(DomainException):
    _DETAIL = 'Account session not found'


class ProviderAlreadyActive(DomainException):
    _DETAIL = 'Provider already active'


class ProviderConfigInvalid(DomainException):
    _DETAIL = 'Provider config invalid.'


class IdentityLoginAlreadyExists(DomainException):
    _DETAIL = 'Identity login already exists'
