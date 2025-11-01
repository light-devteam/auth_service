from src.specifications.binary_logic.base import BinaryLogicSpecification
from src.enums import PostgresBinaryLogicOperators


class AndSpecification(BinaryLogicSpecification):
    _OPERATOR = PostgresBinaryLogicOperators.AND
