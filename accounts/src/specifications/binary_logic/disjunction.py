from src.specifications.binary_logic.base import BinaryLogicSpecification
from src.enums import PostgresBinaryLogicOperators


class OrSpecification(BinaryLogicSpecification):
    _OPERATOR = PostgresBinaryLogicOperators.OR
