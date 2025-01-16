import numpy as np
from src.parser.objects import FunctionDefintion
from src.interpreter.typed_value import VarType, TypedValue

class BuiltInFunction:
    def __init__(self, function):
        self.function = function
        # self.block = self

    def accept(self, visitor):
        visitor.visit_built_in_function(self)

def remove(element, key):
    element.value.pop(key)

def get(element, key):
    return element.value[key]

def printer(*args):
    line = " ".join(str(arg.value) for arg in args)
    print(line)

def add(element, key, value):
    element.value[key] = value

def update(element, key, value):
    element.value[key] = value

def string(element, value):
    val = str(value.value)
    typ = VarType.STRING
    return TypedValue(val, typ)

built_in_functions = {
    'print': BuiltInFunction(printer),
    'remove': BuiltInFunction(remove),
    'get': BuiltInFunction(get),
    'add': BuiltInFunction(add),
    'update': BuiltInFunction(update),
    'str': BuiltInFunction(string)
}