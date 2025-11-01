from typing import Any

from src.specifications.compare import CompareSpecification
from src.enums import PostgresCompareOperators


class IsNullSpecification(CompareSpecification):
    _OPERATOR = PostgresCompareOperators.IS

    def __init__(self, field: str) -> None:
        if not hasattr(self, '_OPERATOR'):
            raise NotImplementedError('Specify OPERATOR in subclass')
        self.field = field
        self.value = 'null'
        self.operator = self._OPERATOR

    def to_sql(self, *args, **kwargs) -> tuple[str, list[Any]]:
        return f'{self.field} {self.operator.value} {self.value}', []
