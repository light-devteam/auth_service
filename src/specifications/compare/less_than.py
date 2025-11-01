from typing import TYPE_CHECKING

from src.specifications.compare.base import CompareSpecification
from src.enums import PostgresCompareOperators

if TYPE_CHECKING:
    from src.specifications.compare.greater_equal import GreaterEqualSpecification


class LessThanSpecification(CompareSpecification):
    _OPERATOR = PostgresCompareOperators.LESS_THAN

    def __invert__(self) -> 'GreaterEqualSpecification':
        from src.specifications.compare.greater_equal import GreaterEqualSpecification
        return GreaterEqualSpecification(self.field, self.value)
