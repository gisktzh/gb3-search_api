from enum import Enum

class QueryOperator(str, Enum):
    AND = "and"
    OR = "or"
    NOT = "not"
