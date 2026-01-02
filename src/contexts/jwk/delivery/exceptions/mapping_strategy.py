from typing import Type

from fastapi import status

from src.domain.exceptions import AppException
from src.delivery.exceptions.base_mapping_strategy import ExceptionMappingStrategy
from src.contexts.jwk.domain import exceptions


class JWKExceptionMapping(ExceptionMappingStrategy):
    @classmethod
    def get_mappings(cls) -> dict[Type[AppException], int]:
        return {
            exceptions.JWKCannotDeactivatePrimary: status.HTTP_409_CONFLICT,
            exceptions.JWKAlreadyPrimary: status.HTTP_409_CONFLICT,
            exceptions.JWKAlreadyExists: status.HTTP_409_CONFLICT,
            exceptions.JWKNotFound: status.HTTP_404_NOT_FOUND,
        }
