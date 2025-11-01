from typing import TypeVar, Generic

from src.specifications.compare.base import CompareSpecification


C = TypeVar('C', bound=CompareSpecification)


class RawSpecification(CompareSpecification, Generic[C]):
    def __init__(self, specification: C) -> None:
        self.__specification = specification

    def to_sql(self, start_index: int = 1) -> tuple[str, list]:
        expression, values = self.__specification.to_sql(start_index)
        expression_without_placeholder = expression[:expression.rfind('$')]
        raw_expression = f'{expression_without_placeholder}{values[0]}'
        return raw_expression, []

    def __invert__(self) -> 'RawSpecification':
        return RawSpecification(~self.__specification)
