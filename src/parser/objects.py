class Node:
    def __init__(self, position) -> None:
        self.position = position

class Program(Node):
    def __init__(self, position, functions) -> None:
        super().__init__(position)
        self.functions = functions
    

class FunctionDefintion(Node):
    def __init__(self, position, type, name, parameters, statements) -> None:
        super().__init__(position)
        self.name = name
        self.parameters = parameters
        self.statements = statements
        self.type = type
    
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
        return (self.key == other.key and 
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
    def __init__(self, position, left, right):
        super().__init__(position)
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, ArthExpression):
            return False
        return (self.left == other.left and 
                self.right == other.right and
                self.position == other.position)

class SumExpression(ArthExpression):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)
    
    def __eq__(self, other):
        if not isinstance(other, SumExpression):
            return False
        return super().__eq__(other)

class SubExpression(ArthExpression):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)
    
    def __eq__(self, other):
        if not isinstance(other, SubExpression):
            return False
        return super().__eq__(other)

class MulExpression(ArthExpression):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)
    
    def __eq__(self, other):
        if not isinstance(other, MulExpression):
            return False
        return super().__eq__(other)

class DivExpression(ArthExpression):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)
    
    def __eq__(self, other):
        if not isinstance(other, ArthExpression):
            return False
        return super().__eq__(other)

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
        return super().__eq__(other)
    
class RelationalExpression(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, RelationalExpression):
            return False
        return super().__eq__(other)

class NotEqualOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, NotEqualOperation):
            return False
        return super().__eq__(other)
        
class GreaterOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, GreaterOperation):
            return False
        return super().__eq__(other)
        
class GreaterEqualOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, GreaterEqualOperation):
            return False
        return super().__eq__(other)
        
class LessOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, LessOperation):
            return False
        return super().__eq__(other)
        
class LessEqualOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def __eq__(self, other):
        if not isinstance(other, LessEqualOperation):
            return False
        return super().__eq__(other)

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
    

class Dictionary(Node):
    def __init__(self, position, dictionary_entries) -> None:
        super().__init__(position)
        self.dictionary_entries = dictionary_entries

    def __eq__(self, other):
        if not isinstance(other, Dictionary):
            return False
        return (self.dictionary_entries == other.dictionary_entries and 
                self.position == other.position)
    
class DictionaryEntry(Node):
    def __init__(self, position, expr1, expr2) -> None:
        super().__init__(position)
        self.expr1 = expr1
        self.expr2 = expr2

    def __eq__(self, other):
        if not isinstance(other, Dictionary):
            return False
        return (self.expr1 == other.expr1 and
                self.expr2 == other.expr2 and  
                self.position == other.position)

class Assignment(Node):
    def __init__(self, position, target, value=None):
        super().__init__(position)
        self.target = target
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Assignment):
            return False
        return (self.target == other.target and 
                self.value == other.value and
                self.position == other.position)


class TypeMatch(Node):
    def __init__(self, position, expression, cases, identifier=None):
        super().__init__(position)
        self.expression = expression
        self.cases = cases
        self.identifier = identifier

    def __eq__(self, other):
        if not isinstance(other, TypeMatch):
            return False
        return (self.expression == other.expression and 
                self.cases == other.cases and
                self.identifier == other.identifier and
                self.position == other.position)
    
class MatchCase(Node):
    def __init__(self, position, type, block):
        super().__init__(position)
        self.type = type
        self.block = block

    def __eq__(self, other):
        if not isinstance(other, MatchCase):
            return False
        return (self.type == other.type and 
                self.block == other.block and
                self.position == other.position)
    

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

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return (self.statements == other.statements and 
                self.position == other.position)
    

class StringType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, StringValue):
            return False
        return True
    

class IntegerType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, IntegerType):
            return False
        return True