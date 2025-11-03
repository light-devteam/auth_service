from src.specifications.unary_logic.base import UnaryLogicSpecification
from src.enums import PostgresUnaryLogicOperators


class NotSpecification(UnaryLogicSpecification):
    _OPERATOR = PostgresUnaryLogicOperators.NOT
