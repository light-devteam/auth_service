from typing import TYPE_CHECKING

from src.specifications.compare.base import CompareSpecification
from src.enums import PostgresCompareOperators

if TYPE_CHECKING:
    from src.specifications.compare.equal import EqualSpecification


class NotEqualSpecification(CompareSpecification):
    _OPERATOR = PostgresCompareOperators.NOT_EQUAL_TO

    def __invert__(self) -> 'EqualSpecification':
        from src.specifications.compare.equal import EqualSpecification
        return EqualSpecification(self.field, self.value)
