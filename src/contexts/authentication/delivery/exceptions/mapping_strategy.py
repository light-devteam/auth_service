from typing import Type

from fastapi import status

from src.domain.exceptions import AppException
from src.delivery.exceptions.base_mapping_strategy import ExceptionMappingStrategy
from src.contexts.authentication.domain import exceptions


class AuthenticationExceptionMapping(ExceptionMappingStrategy):
    @classmethod
    def get_mappings(cls) -> dict[Type[AppException], int]:
        return {
            exceptions.ProviderConfigInvalid: status.HTTP_422_UNPROCESSABLE_CONTENT,
            exceptions.IdentityForProviderAlreadyExists: status.HTTP_409_CONFLICT,
            exceptions.IdentityNotFound: status.HTTP_404_NOT_FOUND,
            exceptions.ProviderAlreadyExists: status.HTTP_409_CONFLICT,
            exceptions.ProviderNotFound: status.HTTP_404_NOT_FOUND,
            exceptions.ProviderNotActive: status.HTTP_403_FORBIDDEN,
            exceptions.AccountNotFound: status.HTTP_404_NOT_FOUND,
            exceptions.ProviderAlreadyActive: status.HTTP_409_CONFLICT,
        }
