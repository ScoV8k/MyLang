from enum import Enum
from src.interpreter.typed_value import VarType

class Variable:
    def __init__(self, value, var_type: VarType):
        self.value = value  
        self.type = var_type      
    
    def __repr__(self):
        return f"Variable(value={self.value}, type={self.type})"
    
    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return (self.value == other.value and 
                self.type == other.type)



