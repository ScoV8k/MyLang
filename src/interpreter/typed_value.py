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
    NULL = "null"


class TypedValue:
    def __init__(self, value, var_type: VarType):
        self.value = value         # rzeczywista wartość
        self.type = var_type       # typ jako VarType (lub cokolwiek innego)
    
    def set_value(self, value):
        self.value = value

    def set_type(self, type):
        self.type = type


    def __repr__(self):
        return f"Variable(value={self.value}, type={self.type})"


