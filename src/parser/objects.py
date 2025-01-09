from abc import abstractmethod
from ..interpreter.visitor import Visitor

class Node:
    def __init__(self, position) -> None:
        self.position = position

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass

    def __str__(self):
        return f"Node(Position: {self.position})"

class Program(Node):
    def __init__(self, position, functions) -> None:
        super().__init__(position)
        self.functions = functions

    def __eq__(self, other):
        if not isinstance(other, Program):
            return False
        return (self.functions == other.functions and 
                self.position == other.position)
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_program(self)
    
    def __str__(self):
        func_str = "\n  ".join(str(func) for func in self.functions)
        return f"Program(Position: {self.position})\n  {func_str}"

class FunctionDefintion(Node):
    def __init__(self, position, type, name, parameters, block) -> None:
        super().__init__(position)
        self.name = name
        self.parameters = parameters
        self.block = block
        self.type = type 

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_function_definition(self)

    def __eq__(self, other):
        if not isinstance(other, FunctionDefintion):
            return False
        return (self.name == other.name and 
                self.parameters == other.parameters and 
                self.block == other.block and 
                self.type == other.type and 
                self.position == other.position)
    
    def __str__(self):
        params_str = ", ".join(str(param) for param in self.parameters)
        # statements_str = "\n    ".join(str(stmt) for stmt in self.block)
        return (f"FunctionDefintion(Name: {self.name}, Type: {self.type}, Position: {self.position})\n"
                f"  Parameters: [{params_str}]\n"
                f"  Statements:\n    {str(self.block)}")

class FunctionArguments(Node):
    def __init__(self, position, arguments) -> None:
        super().__init__(position)
        self.arguments = arguments

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_function_arguments(self)

    def __eq__(self, other):
        if not isinstance(other, FunctionArguments):
            return False
        return (self.arguments == other.arguments and 
                self.position == other.position)


class ReturnStatement(Node):
    def __init__(self, position, expr):
        super().__init__(position)
        self.expr = expr

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_return_statement(self)

    def __eq__(self, other):
        if not isinstance(other, ReturnStatement):
            return False
        return (self.expr == other.expr and 
                self.position == other.position)
    
    def __str__(self):
        return f"ReturnStatement(Position: {self.position}, Expr: {self.expr})"

class Identifier(Node):
    def __init__(self, position, name) -> None:
        super().__init__(position)
        self.name = name

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_identifier(self)

    def __eq__(self, other):
        if not isinstance(other, Identifier):
            return False
        return (self.name == other.name and 
                self.position == other.position)
    
    def __str__(self):
        return f"Identifier(Name: {self.name}, Position: {self.position})"

class Parameter(Node):
    def __init__(self, position, type, name) -> None:
        super().__init__(position)
        self.name = name
        self.type = type

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_parameter(self)

    def __eq__(self, other):
        if not isinstance(other, Parameter):
            return False
        return (self.type == other.type and 
                self.name == other.name and 
                self.position == other.position)

    def __str__(self):
        return f"Parameter(Type: {self.type}, Name: {self.name}, Position: {self.position})"


class ReturnStatement(Node):
    def __init__(self, position, expr):
        super().__init__(position)
        self.expr = expr

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_return_statement(self)

    def __eq__(self, other):
        if not isinstance(other, ReturnStatement):
            return False
        return (self.expr == other.expr and 
                self.position == other.position)

    def __str__(self):
        return f"ReturnStatement(Position: {self.position}, Expr: {self.expr})"


class IfStatement(Node):
    def __init__(self, position, condition, statements, else_statement) -> None:
        super().__init__(position)
        self.condition = condition
        self.statements = statements
        self.else_statement = else_statement

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_if_statement(self)

    def __eq__(self, other):
        if not isinstance(other, IfStatement):
            return False
        return (self.condition == other.condition and 
                self.statements == other.statements and 
                self.else_statement == other.else_statement and 
                self.position == other.position)

    def __str__(self):
        statements_str = "\n    ".join(str(stmt) for stmt in self.statements)
        else_str = f"\n  Else:\n    {self.else_statement}" if self.else_statement else ""
        return (f"IfStatement(Position: {self.position}, Condition: {self.condition})\n"
                f"  Statements:\n    {statements_str}{else_str}")


class WhileStatement(Node):
    def __init__(self, position, condition, statements) -> None:
        super().__init__(position)
        self.condition = condition
        self.statements = statements

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_while_statement(self)

    def __eq__(self, other):
        if not isinstance(other, WhileStatement):
            return False
        return (self.condition == other.condition and 
                self.statements == other.statements and 
                self.position == other.position)
    
    def __str__(self):
        statements_str = "\n    ".join(str(stmt) for stmt in self.statements)
        return (f"WhileStatement(Position: {self.position}, Condition: {self.condition})\n"
                f"  Statements:\n    {statements_str}")


class ForEachStatement(Node):
    def __init__(self, position, key, value, struct, statements) -> None:
        super().__init__(position)
        self.key = key
        self.value = value
        self.struct = struct
        self.statements = statements


    def accept(self, visitor: Visitor) -> None:
        visitor.visit_for_each_statement(self)


    def __eq__(self, other):
        if not isinstance(other, ForEachStatement):
            return False
        return (self.key == other.key and 
                self.value == other.value and 
                self.statements == other.statements and 
                self.struct == other.struct and 
                self.position == other.position)
    

    def __str__(self):
        # statements_str = "\n    ".join(str(stmt) for stmt in self.statements)
        return (f"ForEachStatement(Position: {self.position}, Key: {self.key}, Value: {self.value}, Struct: {self.struct})\n"
                f"  Statements:\n    {self.statements}")


class MultiParameterExpression(Node):
    def __init__(self, position, expressions):
        super().__init__(position)
        self.expressions = expressions

    def __eq__(self, other):
        if not isinstance(other, MultiParameterExpression):
            return False
        return (self.expressions == other.expressions and 
                self.position == other.position)

    def __str__(self):
        expressions_str = ", ".join(str(expr) for expr in self.expressions)
        return f"MultiParameterExpression(Position: {self.position}, Expressions: [{expressions_str}])"


class OrExpression(MultiParameterExpression):
    def __init__(self, position, expressions):
        super().__init__(position, expressions)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_or_expression(self)

    def __eq__(self, other):
        if not isinstance(other, OrExpression):
            return False
        return (self.expressions == other.expressions and 
                self.position == other.position)

    def __str__(self):
        expressions_str = " || ".join(str(expr) for expr in self.expressions)
        return f"OrExpression(Position: {self.position}, Expressions: {expressions_str})"


class AndExpression(MultiParameterExpression):
    def __init__(self, position, expressions):
        super().__init__(position, expressions)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_and_expression(self)

    def __eq__(self, other):
        if not isinstance(other, AndExpression):
            return False
        return (self.expressions == other.expressions and 
                self.position == other.position)

    def __str__(self):
        expressions_str = " && ".join(str(expr) for expr in self.expressions)
        return f"AndExpression(Position: {self.position}, Expressions: {expressions_str})"


class TypeExpression(Node):
    def __init__(self, position, factor, type):
        super().__init__(position)
        self.factor = factor
        self.type = type

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_type_expression(self)

    def __eq__(self, other):
        if not isinstance(other, TypeExpression):
            return False
        return (self.factor == other.factor and 
                self.type == other.type and
                self.position == other.position)

    def __str__(self):
        return f"TypeExpression(Position: {self.position}, Factor: {self.factor}, Type: {self.type})"


class Negation(Node):
    def __init__(self, position, node, negation_type):
        super().__init__(position)
        self.node = node
        self.negation_type = negation_type

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_negation(self)

    def __eq__(self, other):
        if not isinstance(other, Negation):
            return False
        return (self.node == other.node and 
                self.position == other.position and
                self.negation_type == other.negation_type)

    def __str__(self):
        return f"Negation(Position: {self.position}, Node: {self.node})"


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

    def __str__(self):
        return f"ArthExpression(Position: {self.position}, Left: {self.left}, Right: {self.right})"

class SumExpression(ArthExpression):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_sum_expression(self)
    
    def __eq__(self, other):
        if not isinstance(other, SumExpression):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"SumExpression(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class SubExpression(ArthExpression):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_sub_expression(self)
    
    def __eq__(self, other):
        if not isinstance(other, SubExpression):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"SubExpression(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class MulExpression(ArthExpression):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_mul_expression(self)
    
    def __eq__(self, other):
        if not isinstance(other, MulExpression):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"MulExpression(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class DivExpression(ArthExpression):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_div_expression(self) 
    
    def __eq__(self, other):
        if not isinstance(other, DivExpression):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"DivExpression(Position: {self.position}, Left: {self.left}, Right: {self.right})"


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

    def __str__(self):
        return f"BinaryOperation(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class EqualityOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_equality_operation(self)

    def __eq__(self, other):
        if not isinstance(other, EqualityOperation):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"EqualityOperation(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class RelationalExpression(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_relational_operation(self)

    def __eq__(self, other):
        if not isinstance(other, RelationalExpression):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"RelationalExpression(Position: {self.position}, Left: {self.left}, Right: {self.right})"

class NotEqualOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_not_equal_operation(self)

    def __eq__(self, other):
        if not isinstance(other, NotEqualOperation):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"NotEqualOperation(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class GreaterOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_greater_operation(self)

    def __eq__(self, other):
        if not isinstance(other, GreaterOperation):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"GreaterOperation(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class GreaterEqualOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_greater_equal_operation(self)

    def __eq__(self, other):
        if not isinstance(other, GreaterEqualOperation):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"GreaterEqualOperation(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class LessOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_less_operation(self)

    def __eq__(self, other):
        if not isinstance(other, LessOperation):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"LessOperation(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class LessEqualOperation(BinaryOperation):
    def __init__(self, position, left, right):
        super().__init__(position, left, right)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_less_equal_operation(self)

    def __eq__(self, other):
        if not isinstance(other, LessEqualOperation):
            return False
        return super().__eq__(other)

    def __str__(self):
        return f"LessEqualOperation(Position: {self.position}, Left: {self.left}, Right: {self.right})"


class BoolValue(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_bool_value(self)

    def __eq__(self, other):
        if not isinstance(other, BoolValue):
            return False
        return (self.value == other.value and 
                self.position == other.position)

    def __str__(self):
        return f"BoolValue(Position: {self.position}, Value: {self.value})"


class IntegerValue(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_integer_value(self)

    def __eq__(self, other):
        if not isinstance(other, IntegerValue):
            return False
        return (self.value == other.value and 
                self.position == other.position)

    def __str__(self):
        return f"IntegerValue(Position: {self.position}, Value: {self.value})"


class FloatValue(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_float_value(self)
    
    def __eq__(self, other):
        if not isinstance(other, FloatValue):
            return False
        return (self.value == other.value and 
                self.position == other.position)

    def __str__(self):
        return f"FloatValue(Position: {self.position}, Value: {self.value})"


class StringValue(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_string_value(self)

    def __eq__(self, other):
        if not isinstance(other, StringValue):
            return False
        return (self.value == other.value and 
                self.position == other.position)

    def __str__(self):
        return f"StringValue(Position: {self.position}, Value: {self.value})"
    

class NullValue(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_null_value(self)

    def __eq__(self, other):
        if not isinstance(other, NullValue):
            return False
        return (self.value == other.value and 
                self.position == other.position)

    def __str__(self):
        return f"NullValue(Position: {self.position}, Value: {self.value})"
    

class Dictionary(Node):
    def __init__(self, position, dictionary_entries) -> None:
        super().__init__(position)
        self.dictionary_entries = dictionary_entries

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_dictionary(self)

    def __eq__(self, other):
        if not isinstance(other, Dictionary):
            return False
        return (self.dictionary_entries == other.dictionary_entries and 
                self.position == other.position)

    def __str__(self):
        entries_str = ", ".join(str(entry) for entry in self.dictionary_entries)
        return f"Dictionary(Position: {self.position}, Entries: [{entries_str}])"


class DictionaryEntry(Node):
    def __init__(self, position, expr1, expr2) -> None:
        super().__init__(position)
        self.expr1 = expr1
        self.expr2 = expr2

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_dictionary_entry(self)

    def __eq__(self, other):
        if not isinstance(other, DictionaryEntry):
            return False
        return (self.expr1 == other.expr1 and
                self.expr2 == other.expr2 and  
                self.position == other.position)

    def __str__(self):
        return f"DictionaryEntry(Position: {self.position}, Key: {self.expr1}, Value: {self.expr2})"


class Assignment(Node):
    def __init__(self, position, target, value=None):
        super().__init__(position)
        self.target = target
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_assignment(self)

    def __eq__(self, other):
        if not isinstance(other, Assignment):
            return False
        return (self.target == other.target and 
                self.value == other.value and
                self.position == other.position)

    def __str__(self):
        return f"Assignment(Position: {self.position}, Target: {self.target}, Value: {self.value})"


class TypeMatch(Node):
    def __init__(self, position, expression, cases, identifier=None):
        super().__init__(position)
        self.expression = expression
        self.cases = cases
        self.identifier = identifier

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_type_match(self)

    def __eq__(self, other):
        if not isinstance(other, TypeMatch):
            return False
        return (self.expression == other.expression and 
                self.cases == other.cases and
                self.identifier == other.identifier and
                self.position == other.position)

    def __str__(self):
        identifier_str = f", Identifier: {self.identifier}" if self.identifier else ""
        cases_str = "\n  ".join(str(case) for case in self.cases)
        return (f"TypeMatch(Position: {self.position}, Expression: {self.expression}{identifier_str})\n"
                f"  Cases:\n  {cases_str}")


class MatchCase(Node):
    def __init__(self, position, type, block):
        super().__init__(position)
        self.type = type
        self.block = block


    def accept(self, visitor: Visitor) -> None:
        visitor.visit_match_case(self)


    def __eq__(self, other):
        if not isinstance(other, MatchCase):
            return False
        return (self.type == other.type and 
                self.block == other.block and
                self.position == other.position)

    def __str__(self):
        block_str = "\n    ".join(str(stmt) for stmt in self.block)
        return f"MatchCase(Position: {self.position}, Type: {self.type})\n    Block:\n    {block_str}"


class FunctionCall(Node):
    def __init__(self, position, name, arguments=None) -> None:
        super().__init__(position)
        self.function_name = name
        self.arguments = arguments

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_function_call(self)

    def __eq__(self, other):
        if not isinstance(other, FunctionCall):
            return False
        return (self.function_name == other.function_name and 
                self.arguments == other.arguments and
                self.position == other.position)

    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments) if self.arguments else "None"
        return f"FunctionCall(Position: {self.position}, Function: {self.function_name}, Arguments: [{args_str}])"


class ObjectAccess(Node):
    def __init__(self, position, items) -> None:
        super().__init__(position)
        self.items = items

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_object_access(self)

    def __eq__(self, other):
        if not isinstance(other, ObjectAccess):
            return False
        return (self.items == other.items and 
                self.position == other.position)

    def __str__(self):
        calls_str = "\n  ".join(str(call) for call in self.items)
        return (f"ObjectAccess(Position: {self.position})\n"
                f"  Items:\n  {calls_str}")
    
class Block(Node):
    def __init__(self, position, statements) -> None:
        super().__init__(position)
        self.statements = statements

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_block(self)

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return (self.statements == other.statements and 
                self.position == other.position)

    def __str__(self):
        statements_str = "\n  ".join(str(stmt) for stmt in self.statements)
        return f"Block(Position: {self.position})\n  Statements:\n  {statements_str}"


class StringType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_string_type(self)

    def __eq__(self, other):
        if not isinstance(other, StringType):
            return False
        return True

    def __str__(self):
        return f"StringType(Position: {self.position}, Value: {self.value})"


class IntegerType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_integer_type(self)

    def __eq__(self, other):
        if not isinstance(other, IntegerType):
            return False
        return True

    def __str__(self):
        return f"IntegerType(Position: {self.position}, Value: {self.value})"


class BoolType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_bool_type(self)

    def __eq__(self, other):
        if not isinstance(other, BoolType):
            return False
        return True

    def __str__(self):
        return f"BoolType(Position: {self.position}, Value: {self.value})"


class FloatType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_float_type(self)

    def __eq__(self, other):
        if not isinstance(other, FloatType):
            return False
        return True

    def __str__(self):
        return f"FloatType(Position: {self.position}, Value: {self.value})"


class VariantType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_variant_type(self)

    def __eq__(self, other):
        if not isinstance(other, VariantType):
            return False
        return True

    def __str__(self):
        return f"VariantType(Position: {self.position}, Value: {self.value})"


class VoidType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_void_type(self)

    def __eq__(self, other):
        if not isinstance(other, VoidType):
            return False
        return True

    def __str__(self):
        return f"VoidType(Position: {self.position}, Value: {self.value})"

class AnyType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_any_type(self)

    def __eq__(self, other):
        if not isinstance(other, AnyType):
            return False
        return True

    def __str__(self):
        return f"AnyType(Position: {self.position}, Value: {self.value})"
    

class DictionaryType(Node):
    def __init__(self, position, value) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_dictionary_type(self)

    def __eq__(self, other):
        if not isinstance(other, DictionaryType):
            return False
        return True

    def __str__(self):
        return f"DictionaryType(Position: {self.position}, Value: {self.value})"
