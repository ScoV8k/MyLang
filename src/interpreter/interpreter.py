# from .builtins import built_in_functions
from src.parser.objects import FunctionCall, FunctionArguments
from src.interpreter.variable import VarType, Variable
from src.interpreter.typed_value import TypedValue
from src.errors.interpreter_errors import VariableError

class Context:
    def __init__(self):
        self.variables = {}
        self.while_flag = 0
    
    def add_variable(self, name, value, type):
        if name in self.variables:
            raise VariableError(name)
        self.variables[name] = Variable(value, type)

    def reset_flags(self):
        self.break_flag = False

    def has_variable(self, name):
        return name in self.variables
    
    def get_variable(self, name):
        if name not in self.variables:
            raise VariableError(name)
        return self.variables[name]
    
    def get_variable_value(self, name):
        if name not in self.variables:
            raise VariableError(name)
        return self.variables[name].value

    def get_variable_type(self, name):
        if name not in self.variables:
            raise VariableError(name)
        return self.variables[name].type
    
    def set_variable(self, name, value):
        if name not in self.variables:
            raise VariableError(name)
        self.variables[name].value = value

    def new_context(self):
        return Context()


class Interpreter:
    def __init__(self, program):
        self.program = program

    def execute(self, visitor):
        self.program.accept(visitor)
        ret_code = visitor.last_result if visitor.last_result is not None else 0
        return ret_code.value