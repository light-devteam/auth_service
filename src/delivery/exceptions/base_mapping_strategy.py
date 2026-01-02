from abc import ABC, abstractmethod
from typing import Type

from src.domain.exceptions import AppException


class ExceptionMappingStrategy(ABC):
    @classmethod
    @abstractmethod
    def get_mappings(cls) -> dict[Type[AppException], int]:
        ...
