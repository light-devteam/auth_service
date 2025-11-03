from typing import TYPE_CHECKING

from src.specifications.compare.base import CompareSpecification
from src.enums import PostgresCompareOperators

if TYPE_CHECKING:
    from src.specifications.compare.greater_than import GreaterThanSpecification


class LessEqualSpecification(CompareSpecification):
    _OPERATOR = PostgresCompareOperators.LESS_THAN_OR_EQUAL_TO

    def __invert__(self) -> 'GreaterThanSpecification':
        from src.specifications.compare.greater_than import GreaterThanSpecification
        return GreaterThanSpecification(self.field, self.value)
