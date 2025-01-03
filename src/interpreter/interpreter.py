# from .builtins import built_in_functions
from src.parser.objects import FunctionCall, FunctionArguments
    
class Context:
    def __init__(self):
        self.variables = {}
        self.while_flag = 0 # licznik while
    
    def reset_flags(self):
        self.return_flag = False

    def add_variable(self, name, value):
        if isinstance(value, list):
            if name in self.variables:
                self.variables[name].set_value(value)
        else:
            self.variables[name] = value

    def get_variable(self, name):
        if name not in self.variables:
            raise KeyError(f"Variable '{name}' is not defined.")
        return self.variables.get(name)

    def new_context(self):
        return Context()


class Interpreter:
    def __init__(self, program):
        self.program = program
    
    def get_nested_value(self, data):
        if hasattr(data, 'value'):
            return self.get_nested_value(data.value)
        else:
            return data

    def execute(self, visitor):
        self.program.accept(visitor)
        main_call = FunctionCall(visitor.functions.get('main').position, 'main', [])
        main_call.accept(visitor)
        ret_code = visitor.last_result if visitor.last_result is not None else 0
        return self.get_nested_value(ret_code)
