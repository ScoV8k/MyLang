# from .builtins import built_in_functions
from src.parser.objects import FunctionCall, FunctionArguments
    
class Context:
    def __init__(self):
        self.variables = {}
        self.while_flag = 0 # licznik while
    
    def add_variable(self, name, value, type):
        if name in self.variables:
            raise NameError(f"Zmienna {name} jest juz zdefiniowana.")
        self.variables[name] = {
            'value': value,
            'type': type
        }

    def has_variable(self, name):
        return name in self.variables
    
    def get_variable(self, name):
        if name not in self.variables:
            raise KeyError(f"Zmienna {name} nie została zdefiniowana.")
        return self.variables[name]
    
    def get_variable_value(self, name):
        if name not in self.variables:
            raise NameError(f"Zmienna '{name}' nie została zadeklarowana!")
        return self.variables[name]['value']

    def get_variable_type(self, name):
        if name not in self.variables:
            raise NameError(f"Zmienna '{name}' nie została zadeklarowana!")
        return self.variables[name]['type']
    
    def set_variable(self, name, value):
        if name not in self.variables:
            raise NameError(f"Zmienna {name} nie jest zadeklarowana!")
        # Opcjonalne sprawdzenie zgodności typu
        # if not self._check_type_compatibility(value, self.variables[name]['type']):
        #     raise TypeMismatchError(...)
        self.variables[name]['value'] = value

    def new_context(self):
        return Context()


class Interpreter:
    def __init__(self, program):
        self.program = program
    
    def get_nested_value(self, data):
        while hasattr(data, 'value'):
            data = data.value
        return data


    def execute(self, visitor):
        self.program.accept(visitor)
        main_call = FunctionCall(visitor.functions.get('main').position, 'main', [])
        main_call.accept(visitor) # wewnątrz wizytacji programu
        ret_code = visitor.last_result if visitor.last_result is not None else 0
        return self.get_nested_value(ret_code) # return ret_code.value
