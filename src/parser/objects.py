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
    def __init__(self, position, name, parameters, statements) -> None:
        super().__init__(position)
        self.name = name
        self.parameters = parameters
        self.statements = statements
    
    def __str__(self):
        parameters_str = ", ".join(str(param) for param in self.parameters)
        statements_str = "\n    ".join(str(stmt) for stmt in self.statements)
        return f'Function "{self.name}":\n  Parameters: {parameters_str}\n  Statements:\n    {statements_str}'
    
    def __eq__(self, other):
        if not isinstance(other, FunctionDefintion):
            return False
        return (self.position == other.position and 
                self.name == other.name and 
                self.parameters== other.parameters and
                self.statements == other.statements)

# class IncludeStatement(Node):
#     def __init__(self, position, library_name, objects_names) -> None:
#         super().__init__(position)
#         self.library_name = library_name
#         self.objects_names = objects_names

#     def __str__(self):
#         objects_names = ", ".join(str(object.name) for object in self.objects_names)
#         return f'Include {self.library_name} with objects {objects_names}'

# class LambdaExpression(Node):
#     def __init__(self, position, variable_name, statements) -> None:
#         super().__init__(position)
#         self.variable_name = variable_name
#         self.statements = statements

#     def __str__(self):
#         statements = "\n ".join(str(stmt) for stmt in self.statements)
#         return f'Lambda {self.variable_name} with statements: {statements}'

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

#     def __str__(self):
#         stmts_str = "\n".join(str(stmt) for stmt in self.statements)
#         return f'While {self.condition} do:\n    {stmts_str}'

# class BreakStatement(Node):
#     def __str__(self):
#         return f'BreakStatement at {self.position}'

# class MultiParameterExpression(Node):
#     def __init__(self, position, nodes):
#         super().__init__(position)
#         self.nodes = nodes
        
#     def __str__(self):
#         nodes_str = ', '.join(str(node) for node in self.nodes)
#         return f'{self.__class__.__name__}({nodes_str})'

# class OrExpression(MultiParameterExpression):
#     def __init__(self, position, nodes):
#         super().__init__(position, nodes)

#     def __str__(self):
#         return super().__str__()
        
# class AndExpression(MultiParameterExpression):
#     def __init__(self, position, nodes):
#         super().__init__(position, nodes)

#     def __str__(self):
#         return super().__str__()

# class Negation(Node):
#     def __init__(self, position, node):
#         super().__init__(position)
#         self.node = node
        
#     def __str__(self):
#         return f'Negation of ({self.node}) at {self.position}'

# class ArthExpression(Node):
#     def __init__(self, position, node):
#         super().__init__(position)
#         self.node = node

#     def __str__(self):
#         return super().__str__()

# class SumExpression(ArthExpression):
#     def __init__(self, position, node):
#         super().__init__(position, node)
    
#     def __str__(self):
#         return super().__str__()

# class SubExpression(ArthExpression):
#     def __init__(self, position, node):
#         super().__init__(position, node)
    
#     def __str__(self):
#         return super().__str__()

# class MulExpression(ArthExpression):
#     def __init__(self, position, node):
#         super().__init__(position, node)
    
#     def __str__(self):
#         return super().__str__()

# class DivExpression(ArthExpression):
#     def __init__(self, position, node):
#         super().__init__(position, node)
    
#     def __str__(self):
#         return super().__str__()

# class BinaryOperation(Node):
#     def __init__(self, position, left, right):
#         super().__init__(position)
#         self.left = left
#         self.right = right
        
#     def __str__(self):
#         return f'{str(self.left)} {self.__class__.__name__} {str(self.right)}'

# class EqualOperation(BinaryOperation):
#     def __init__(self, position, left, right):
#         super().__init__(position, left, right)

#     def __str__(self):
#         return super().__str__()

# class NotEqualOperation(BinaryOperation):
#     def __init__(self, position, left, right):
#         super().__init__(position, left, right)

#     def __str__(self):
#         return super().__str__()
        
# class GreaterOperation(BinaryOperation):
#     def __init__(self, position, left, right):
#         super().__init__(position, left, right)

#     def __str__(self):
#         return super().__str__()
        
# class GreaterEqualOperation(BinaryOperation):
#     def __init__(self, position, left, right):
#         super().__init__(position, left, right)

#     def __str__(self):
#         return super().__str__()
        
# class LessOperation(BinaryOperation):
#     def __init__(self, position, left, right):
#         super().__init__(position, left, right)

#     def __str__(self):
#         return super().__str__()
        
# class LessEqualOperation(BinaryOperation):
#     def __init__(self, position, left, right):
#         super().__init__(position, left, right)

#     def __str__(self):
#         return super().__str__()

# class LiteralBool(Node):
#     def __init__(self, position, value) -> None:
#         super().__init__(position)
#         self.value = value

#     def __str__(self):
#         return f'{self.value} at {self.position}'

# class LiteralInt(Node):
#     def __init__(self, position, value) -> None:
#         super().__init__(position)
#         self.value = value

#     def __str__(self):
#         return f'Integer value {self.value}'

# class LiteralFloat(Node):
#     def __init__(self, position, value) -> None:
#         super().__init__(position)
#         self.value = value
    
#     def __str__(self):
#         return f'Float value {self.value}'

# class LiteralString(Node):
#     def __init__(self, position, value) -> None:
#         super().__init__(position)
#         self.value = value

#     def __str__(self):
#         return f'String value "{self.value}"'

# class Array(Node):
#     def __init__(self, position, items) -> None:
#         super().__init__(position)
#         self.items = items
    
#     def __str__(self):
#         items_str = ', '.join(str(item) for item in self.items)
#         return f'Array [{items_str}]'

# class Assignment(Node):
#     def __init__(self, position, target, value):
#         super().__init__(position)
#         self.target = target
#         self.value = value

#     def __str__(self):
#         return f'VariableAssignment of {str(self.target)} to {str(self.value)}'

class FunctionCall(Node):
    def __init__(self, position, function_name, arguments) -> None:
        super().__init__(position)
        self.function_name = function_name
        self.arguments = arguments
    
    def __eq__(self, other):
        if not isinstance(other, FunctionCall):
            return False
        return (self.function_name == other.function_name and 
                self.arguments == other.arguments and
                self.position == other.position)
    
class Block(Node):
    def __init__(self, position, statements) -> None:
        super().__init__(position)
        self.statements = statements