from typing import TYPE_CHECKING

from src.specifications.compare.base import CompareSpecification
from src.enums import PostgresCompareOperators

if TYPE_CHECKING:
    from src.specifications.compare.less_than import LessThanSpecification


class GreaterEqualSpecification(CompareSpecification):
    _OPERATOR = PostgresCompareOperators.GREATER_THAN_OR_EQUAL_TO

    def __invert__(self) -> 'LessThanSpecification':
        from src.specifications.compare.less_than import LessThanSpecification
        return LessThanSpecification(self.field, self.value)
