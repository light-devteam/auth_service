from enum import StrEnum


class PostgresCompareOperators(StrEnum):
    EQUAL_TO = '='
    NOT_EQUAL_TO = '!='
    GREATER_THAN = '>'
    LESS_THAN = '<'
    GREATER_THAN_OR_EQUAL_TO = '>='
    LESS_THAN_OR_EQUAL_TO = '<='
    IS = 'IS'
