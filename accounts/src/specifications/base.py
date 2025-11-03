from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.specifications.unary_logic import NotSpecification
    from src.specifications.binary_logic import AndSpecification, OrSpecification


class BaseSpecification(ABC):
    @abstractmethod
    def to_sql(self, start_index: int = 1) -> tuple[str, list[Any]]:
        raise NotImplementedError()

    def __and__(self, other: 'BaseSpecification') -> 'AndSpecification':
        from src.specifications.binary_logic import AndSpecification
        return AndSpecification(self, other)

    def __or__(self, other: 'BaseSpecification') -> 'OrSpecification':
        from src.specifications.binary_logic import OrSpecification
        return OrSpecification(self, other)

    def __invert__(self) -> 'NotSpecification':
        from src.specifications.unary_logic import NotSpecification
        return NotSpecification(self)

    def __neg__(self) -> 'NotSpecification':
        return self.__invert__()
