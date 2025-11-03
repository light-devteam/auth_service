from typing import Any

from src.specifications.base import BaseSpecification
from src.enums import PostgresCompareOperators


class CompareSpecification(BaseSpecification):
    _OPERATOR: PostgresCompareOperators

    def __init__(self, field: str, value: Any) -> None:
        if not hasattr(self, '_OPERATOR'):
            raise NotImplementedError('Specify OPERATOR in subclass')
        self.field = field
        self.value = value
        self.operator = self._OPERATOR

    def to_sql(self, start_index: int = 1) -> tuple[str, list[Any]]:
        return f'{self.field} {self.operator.value} ${start_index}', [self.value]
