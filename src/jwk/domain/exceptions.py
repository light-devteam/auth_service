from src.shared.domain import exceptions


class JWKNotFound(exceptions.DomainException):
    _DETAIL = 'JWK not found'


class JWKAlreadyExists(exceptions.DomainException):
    _DETAIL = 'JWK with same name already exists'


class JWKAlreadyPrimary(exceptions.DomainException):
    _DETAIL = 'JWK already primary'


class JWKCannotDeactivatePrimary(exceptions.DomainException):
    _DETAIL = 'Primary JWK needs to be always active'
