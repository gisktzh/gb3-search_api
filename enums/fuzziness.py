from enum import Enum

class Fuzziness(str, Enum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    AUTO = "AUTO"
