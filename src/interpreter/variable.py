from enum import Enum

class VarType(Enum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    DICT = "dict"
    ANY = "any"
    VOID = "void"
    VARIANT = "variant"


class Variable:
    def __init__(self, value, var_type: VarType):
        self.value = value         # rzeczywista wartość
        self.type = var_type       # typ jako VarType (lub cokolwiek innego)
    
    def __repr__(self):
        return f"Variable(value={self.value}, type={self.type})"


