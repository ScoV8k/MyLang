import numpy as np
from src.parser.objects import FunctionDefintion

class BuiltInFunction:
    def __init__(self, function):
        self.function = function
        self.block = self

    def accept(self, visitor):
        visitor.visit_built_in_function(self)

def remove(element, key):
    element.value.pop(key)

def get(element, key):
    return element.value[key]

def printer(text):
    print(text.value)

def add(element, key, value):
    element.value[key] = value

def update(element, key, value):
    element.value[key] = value

# klasa reprezentująca funkcję wbudowaną
built_in_functions = {
    'print': BuiltInFunction(printer),
    'remove': BuiltInFunction(remove),
    'get': BuiltInFunction(get),
    'add': BuiltInFunction(add),
    'update': BuiltInFunction(update)
}