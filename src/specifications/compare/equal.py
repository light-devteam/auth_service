from typing import TYPE_CHECKING

from src.specifications.compare.base import CompareSpecification
from src.enums import PostgresCompareOperators

if TYPE_CHECKING:
    from src.specifications.compare.not_equal import NotEqualSpecification


class EqualSpecification(CompareSpecification):
    _OPERATOR = PostgresCompareOperators.EQUAL_TO

    def __invert__(self) -> 'NotEqualSpecification':
        from src.specifications.compare.not_equal import NotEqualSpecification
        return NotEqualSpecification(self.field, self.value)
