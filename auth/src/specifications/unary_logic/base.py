from typing import Any

from src.specifications.base import BaseSpecification
from src.enums import PostgresUnaryLogicOperators


class UnaryLogicSpecification(BaseSpecification):
    _OPERATOR: PostgresUnaryLogicOperators

    def __init__(self, specification: BaseSpecification) -> None:
        if not hasattr(self, '_OPERATOR'):
            raise NotImplementedError('Specify OPERATOR in subclass')
        self.specification = specification
        self.operator = self._OPERATOR

    def to_sql(self, start_index: int = 1) -> tuple[str, list[Any]]:
        sql, parameters = self.specification.to_sql(start_index)
        return f'{self.operator} ({sql})', parameters
