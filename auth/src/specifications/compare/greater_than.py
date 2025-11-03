from typing import TYPE_CHECKING

from src.specifications.compare.base import CompareSpecification
from src.enums import PostgresCompareOperators

if TYPE_CHECKING:
    from src.specifications.compare.less_equal import LessEqualSpecification


class GreaterThanSpecification(CompareSpecification):
    _OPERATOR = PostgresCompareOperators.GREATER_THAN

    def __invert__(self) -> 'LessEqualSpecification':
        from src.specifications.compare.less_equal import LessEqualSpecification
        return LessEqualSpecification(self.field, self.value)
