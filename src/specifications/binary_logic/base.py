from typing import Any

from src.specifications.base import BaseSpecification
from src.enums import PostgresBinaryLogicOperators


class BinaryLogicSpecification(BaseSpecification):
    _OPERATOR: PostgresBinaryLogicOperators

    def __init__(self, *specifications: BaseSpecification) -> None:
        if not hasattr(self, '_OPERATOR'):
            raise NotImplementedError('Specify OPERATOR in subclass')
        self.specifications = specifications
        self.operator = self._OPERATOR

    def to_sql(self, start_index: int = 1) -> tuple[str, list[Any]]:
        sql_parts = []
        parameters = []
        index = start_index
        for specification in self.specifications:
            specification_sql, specification_parameters = specification.to_sql(index)
            sql_parts.append(f'({specification_sql})')
            parameters.extend(specification_parameters)
            index += len(specification_parameters)
        return f' {self.operator} '.join(sql_parts), parameters
