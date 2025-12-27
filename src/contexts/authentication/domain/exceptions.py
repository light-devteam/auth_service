from src.domain.exceptions import DomainException


class ProviderNotActive(DomainException):
    _DETAIL = 'Provider not active'


class IdentityAlreadyMain(DomainException):
    _DETAIL = 'Identity already set as main for this account'


class MainIdentityAlreadySet(DomainException):
    _DETAIL = 'Account must be have only one main identity'


class IdentityForProviderAlreadyExists(DomainException):
    _DETAIL = 'Identity for this provider already exists'


class SessionAlreadyRevoked(DomainException):
    _DETAIL = 'Account session already has been revoked'


class TokenAlreadyRevoked(DomainException):
    _DETAIL = 'Session refresh token already has been revoked'
