class Node:
    def __init__(self, position) -> None:
        self.position = position

class Program(Node):
    def __init__(self, position, functions) -> None:
        super().__init__(position)
        self.functions = functions
    
    def __str__(self):
        function_definitions = '\n'.join(str(self.functions[function]) for function in self.functions)
        return f"Program na pozycji {self.position} z funkcjami:\n{function_definitions}"

class FunctionDefintion(Node):
    def __init__(self, position, type, name, parameters, statements) -> None:
        super().__init__(position)
        self.name = name
        self.parameters = parameters
        self.statements = statements
        self.type = type
    
    def __str__(self):
        parameters_str = ", ".join(str(param) for param in self.parameters)
        statements_str = "\n    ".join(str(stmt) for stmt in self.statements)
        return f'Function "{self.name}":\n  Parameters: {parameters_str}\n  Statements:\n    {statements_str}'
    
    def __eq__(self, other):
        if not isinstance(other, FunctionDefintion):
            return False
        return (self.position == other.position and 
                self.type == other.type and 
                self.name == other.name and 
                self.parameters== other.parameters and
                self.statements == other.statements)

class FunctionArguments(Node):
    def __init__(self, position, arguments) -> None:
        super().__init__(position)
        self.arguments = arguments

    def __str__(self):
        args = ", ".join(str(object) for object in self.arguments)
        return f'FunctionArguments: {args}'

class Identifier(Node):
    def __init__(self, position, name) -> None:
        super().__init__(position)
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Identifier):
            return False
        return (self.name == other.name and 
                self.position == other.position)
    

class Parameter(Node):
    def __init__(self, position, type, name) -> None:
        super().__init__(position)
        self.name = name
        self.type = type
    
    def __str__(self):
        return f'Parameter "{self.name}"'
    
    def __eq__(self, other):
        if not isinstance(other, Parameter):
            return False
        return (self.type == other.type and 
                self.name == other.name and 
                self.position == other.position)

class ReturnStatement(Node):
    def __init__(self,position, expr):
        super().__init__(position)
        self.expr = expr
        
    def __eq__(self, other):
        if not isinstance(other, ReturnStatement):
            return False
        return (self.expr == other.expr and 
                self.position == other.position)

class IfStatement(Node):
    def __init__(self, position, condition, statements, else_statement) -> None:
        super().__init__(position)
        self.condition = condition
        self.statements = statements
        self.else_statement = else_statement

    def __str__(self):
        if_statements_str = "\n     ".join(str(stmt) for stmt in self.statements)
        else_statement_str = "\n    ".join(str(stmt) for stmt in self.else_statement)
        return f'If {self.condition}:\n  Then:\n    {if_statements_str}\n  Else:\n    {else_statement_str}'
    
    def __eq__(self, other):
        if not isinstance(other, IfStatement):
            return False
        return (self.type == other.type and 
                self.name == other.name and 
                self.position == other.position)

class WhileStatement(Node):
    def __init__(self, position, condition, statements) -> None:
        super().__init__(position)
        self.condition = condition
        self.statements = statements

    def __eq__(self, other):
        if not isinstance(other, WhileStatement):
            return False
        return (self.condition == other.condition and 
                self.statements == other.statements and 
                self.position == other.position)
    
class ForEachStatement(Node):
    def __init__(self, position, key, value, struct, statements) -> None:
        super().__init__(position)
        self.key = key
        self.value = value
        self.struct = struct
        self.statements = statements

    def __eq__(self, other):
        if not isinstance(other, ForEachStatement):
            return False
        return (self.key == other.ley and 
                self.value == other.value and 
                self.struct == other.struct and
                self.statements == other.statements and
                self.position == other.position)


class MultiParameterExpression(Node):
    def __init__(self, position, expressions):
        super().__init__(position)
        self.expressions = expressions
        
    def __eq__(self, other):
        if not isinstance(other, MultiParameterExpression):
            return False
        return (self.expressions == other.expressions and 
                self.position == other.position)

class OrExpression(MultiParameterExpression):
    def __init__(self, position, expressions):
        super().__init__(position, expressions)

    def __eq__(self, other):
        if not isinstance(other, OrExpression):
            return False
        return (self.expressions == other.expressions and 
                self.position == other.position)
        
class AndExpression(MultiParameterExpression):
    def __init__(self, position, expressions):
        super().__init__(position, expressions)

    def __eq__(self, other):
        if not isinstance(other, AndExpression):
            return False
        return (self.expressions == other.expressions and 
                self.position == other.position)
    

class TypeExpression(Node):
    def __init__(self, position, factor, type):
        super().__init__(position)
        self.factor = factor
        self.type = type
        
    def __eq__(self, other):
        if not isinstance(other, TypeExpression):
            return False
        return (self.factor == other.factor and 
                self.type == other.type and
                self.position == other.position)
    

class Negation(Node):
    def __init__(self, position, node):
        super().__init__(position)
        self.node = node
        
    def __eq__(self, other):
        if not isinstance(other, Negation):
            return False
        return (self.node == other.node and 
                self.position == other.position)

class ArthExpression(Node):
    def __init__(self, position, node):
        super().__init__(position)
        self.node = node

    def __eq__(self, other):
        if not isinstance(other, ArthExpression):
            return False
        return (self.node == other.node and 
                self.position == other.position)

class SumExpression(ArthExpression):
    def __init__(self, position, node):
        super().__init__(position, node)
    
    def __eq__(self, other):
        if not isinstance(other, SumExpression):
            return False
        return (self.node == other.node and 
                self.position == other.position)

class SubExpression(ArthExpression):
    def __init__(self, position, node):
        super().__init__(position, node)
    
    def __eq__(self, other):
        if not isinstance(other, SubExpression):
            return False
        return (self.node == other.node and 
                self.position == other.position)

class MulExpression(ArthExpression):
    def __init__(self, position, node):
        super().__init__(position, node)
    
    def __eq__(self, other):
        if not isinstance(other, MulExpression):
            return False
        return (self.node == other.node and 
                self.position == other.position)

class DivExpression(ArthExpression):
    def __init__(self, position, node):
        super().__init__(position, node)
    
    def __eq__(self, other):
        if not isinstance(other, DivExpression):
            return False
        return (self.node == other.node and 
                self.position == other.position)

class BinaryOperation(Node):
    def __init__(self, position, left, right):
        super().__init__(position)
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, BinaryOperation):
            return False
        return (self.left == other.left and 
                self.right == other.right and 
                self.position == other.position)
        
class EqualityOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, EqualityOperation):
            return False
        return (self.left == other.left and 
                self.right == other.right and 
                self.position == other.position)
    
class RelationalExpression(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, RelationalExpression):
            return False
        return (self.left == other.left and 
                self.right == other.right and 
                self.position == other.position)

class NotEqualOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, NotEqualOperation):
            return False
        return (self.left == other.left and 
                self.right == other.right and 
                self.position == other.position)
        
class GreaterOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, GreaterOperation):
            return False
        return (self.left == other.left and 
                self.right == other.right and 
                self.position == other.position)
        
class GreaterEqualOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, GreaterEqualOperation):
            return False
        return (self.left == other.left and 
                self.right == other.right and 
                self.position == other.position)
        
class LessOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, LessOperation):
            return False
        return (self.left == other.left and 
                self.right == other.right and 
                self.position == other.position)
        
class LessEqualOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, LessEqualOperation):
            return False
        return (self.left == other.left and 
                self.right == other.right and 
                self.position == other.position)

class BoolValue(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, BoolValue):
            return False
        return (self.value == other.value and 
                self.position == other.position)

class IntegerValue(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, IntegerValue):
            return False
        return (self.value == other.value and 
                self.position == other.position)

class FloatValue(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value
    
    def __eq__(self, other):
        if not isinstance(other, FloatValue):
            return False
        return (self.value == other.value and 
                self.position == other.position)

class StringValue(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, StringValue):
            return False
        return (self.value == other.value and 
                self.position == other.position)

class Assignment(Node):
    def __init__(self, position, target, value):
        super().__init__(position)
        self.target = target
        self.value = value

    def __str__(self):
        return f'VariableAssignment of {str(self.target)} to {str(self.value)}'

class FunctionCall(Node):
    def __init__(self, position, function_name, arguments=None) -> None:
        super().__init__(position)
        self.function_name = function_name
        self.arguments = arguments
    
    def __eq__(self, other):
        if not isinstance(other, FunctionCall):
            return False
        return (self.function_name == other.function_name and 
                self.arguments == other.arguments and
                self.position == other.position)
    
class ObjectAccess(Node):
    def __init__(self, position, item, function_calls) -> None:
        super().__init__(position)
        self.item = item
        self.function_calls = function_calls
    
    def __eq__(self, other):
        if not isinstance(other, ObjectAccess):
            return False
        return (self.item == other.item and 
                self.function_calls == other.function_calls and
                self.position == other.position)
    
class Block(Node):
    def __init__(self, position, statements) -> None:
        super().__init__(position)
        self.statements = statements