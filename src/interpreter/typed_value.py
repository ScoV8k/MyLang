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
        self.value = value      
        self.type = var_type       
    
    def set_value(self, value):
        self.value = value

    def set_type(self, type):
        self.type = type

    def __repr__(self):
        return f"Variable(value={self.value}, type={self.type})"

    def __eq__(self, other):
        if not isinstance(other, TypedValue):
            return False
        return (self.value == other.value and 
                self.type == other.type)

    def __hash__(self):
        # Zakładając, że self.value i self.type są same w sobie
        # haszowalne (np. self.value to int, float, str, bool lub None)
        # można zrobić wprost:
        return hash((self.value, self.type))