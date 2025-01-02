from src.interpreter.visitor import Visitor
from src.parser.objects import *

class PrintVisitor(Visitor):
    def __init__(self):
        self.indent_level = 0

    def _print_indent(self, text):
        print( "   " * self.indent_level  + text)

    def visit_program(self, program: Program):
        self._print_indent(f"Program at {program.position}")
        self.indent_level += 1
        for function in program.functions:
            function.accept(self)
        self.indent_level -= 1

    def visit_function_definition(self, node: FunctionDefintion):
        self._print_indent(f"Function \"{node.name}\" at {node.position}")
        self.indent_level += 1
        params = ", ".join(obj for obj in node.parameters)
        self._print_indent(f"With parameters: \"{params}\"")
        node.block.accept(self)
        self.indent_level -= 1

    def visit_function_arguments(self, element: FunctionArguments):
        return super().visit_function_arguments(element)
    
    def visit_return_statement(self, node: ReturnStatement):
        self._print_indent(f"ReturnStatement at {node.position}")
        self.indent_level += 1
        node.statement.accept(self)
        self.indent_level -= 1

    def visit_identifier(self, node: Identifier):
        self._print_indent(f"Identifier \"{node.name}\" at {node.position}")

    def visit_parameter(self, node: Parameter):
        self._print_indent(f"Parameter \"{node.name}\" at {node.position}")

    def visit_if_statement(self, node: IfStatement):
        self._print_indent(f"If statement at {node.position} with condition:")
        self.indent_level += 1
        node.condition.accept(self)
        self._print_indent("Then:")
        self.indent_level += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.indent_level -= 1
        if node.else_statement:
            self._print_indent("Else:")
            self.indent_level += 1
            for stmt in node.else_statement:
                stmt.accept(self)
            self.indent_level -= 1
        self.indent_level -= 1

    def visit_while_statement(self, node: WhileStatement):
        self._print_indent(f"While statement at {node.position} with condition:")
        self.indent_level += 1
        node.condition.accept(self)
        self._print_indent("Do:")
        self.indent_level += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.indent_level -= 1
        self.indent_level -= 1

    def visit_for_each_statement(self, node: ForEachStatement):
        self._print_indent(f"ForEachStatement at {node.position}")
        self.indent_level += 1
        self._print_indent(f"Key: {node.key}, Value: {node.value}")
        node.struct.accept(self)
        for stmt in node.statements.statements:
            stmt.accept(self)
        self.indent_level -= 1

    def visit_or_expression(self, node: OrExpression):
        self._print_indent(f"OrExpression at {node.position}")
        self.indent_level += 1
        for expr in node.nodes:
            expr.accept(self)
        self.indent_level -= 1

    def visit_and_expression(self, node: AndExpression):
        self._print_indent(f"AndExpression at {node.position}")
        self.indent_level += 1
        for expr in node.nodes:
            expr.accept(self)
        self.indent_level -= 1

    def visit_type_expression(self, node: TypeExpression):
        self._print_indent(f"TypeExpression at {node.position}")
        self.indent_level += 1
        node.factor.accept(self)
        self._print_indent(f"Type: {node.type}")
        self.indent_level -= 1

    def visit_negation(self, node: Negation):
        self._print_indent(f"Negation of type {node.negation_type} at {node.position}")
        self.indent_level += 1
        node.node.accept(self)
        self.indent_level -= 1

    def visit_sum_expression(self, node: SumExpression):
        self._print_indent(f"SumExpression at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_sub_expression(self, node: SubExpression):
        self._print_indent(f"SubExpression at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_mul_expression(self, node: MulExpression):
        self._print_indent(f"MulExpression at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_div_expression(self, node: DivExpression):
        self._print_indent(f"DivExpression at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_equality_operation(self, node: EqualityOperation):
        self._print_indent(f"EqualityOperation at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_relational_operation(self, node: RelationalExpression):
        self._print_indent(f"RelationalExpression at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_not_equal_operation(self, node: NotEqualOperation):
        self._print_indent(f"NotEqualOperation at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_greater_operation(self, node: GreaterOperation):
        self._print_indent(f"GreaterOperation at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_greater_equal_operation(self, node:GreaterEqualOperation):
        self._print_indent(f"GreaterEqualOperation at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_less_operation(self, node: LessOperation):
        self._print_indent(f"LessOperation at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_less_equal_operation(self, node: LessEqualOperation):
        self._print_indent(f"LessEqualOperation at {node.position}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1

    def visit_bool_value(self, node: BoolValue):
        self._print_indent(f"BoolValue {node.value} at {node.position}")

    def visit_integer_value(self, node: IntegerValue):
        self._print_indent(f"IntegerValue {node.value} at {node.position}")

    def visit_float_value(self, node: FloatValue):
        self._print_indent(f"FloatValue {node.value} at {node.position}")

    def visit_string_value(self, node: StringValue):
        self._print_indent(f"StringValue \"{node.value}\" at {node.position}")

    def visit_dictionary(self, node: Dictionary):
        self._print_indent(f"Dictionary at {node.position}")
        self.indent_level += 1
        for entry in node.dictionary_entries:
            entry.accept(self)
        self.indent_level -= 1

    def visit_dictionary_entry(self, node: DictionaryEntry):
        self._print_indent(f"DictionaryEntry at {node.position}")
        self.indent_level += 1
        node.expr1.accept(self)
        node.expr2.accept(self)
        self.indent_level -= 1

    def visit_assignment(self, node: Assignment):
        self._print_indent(f"Assignment at {node.position}")
        self.indent_level += 1
        node.target.accept(self)
        node.value.accept(self)
        self.indent_level -= 1

    def visit_type_match(self, node: TypeMatch):
        self._print_indent(f"TypeMatch at {node.position}")
        self.indent_level += 1
        node.expression.accept(self)
        for case in node.cases:
            case.accept(self)
        self.indent_level -= 1

    def visit_match_case(self, node: MatchCase):
        self._print_indent(f"MatchCase at {node.position}")
        self.indent_level += 1
        self._print_indent(f"Type: {node.type}")
        for stmt in node.block:
            stmt.accept(self)
        self.indent_level -= 1

    def visit_function_call(self, node: FunctionCall):
        self._print_indent(f"FunctionCall to {node.function_name} at {node.position}")
        self.indent_level += 1
        for argument in node.arguments:
            argument.accept(self)
        self.indent_level -= 1

    def visit_object_access(self, node: ObjectAccess):
        self._print_indent(f"ObjectAccess at {node.position}")
        self.indent_level += 1
        for item in node.items:
            item.accept(self)
        self.indent_level -= 1

    def visit_block(self, node: Block):
        self._print_indent(f"Block at {node.position}")
        self.indent_level += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.indent_level -= 1

    def visit_string_type(self, node: StringType):
        self._print_indent(f"StringType at {node.position}, Value: {node.value}")

    def visit_integer_type(self, node: IntegerType):
        self._print_indent(f"IntegerType at {node.position}, Value: {node.value}")

    def visit_bool_type(self, node: BoolType):
        self._print_indent(f"BoolType at {node.position}, Value: {node.value}")

    def visit_float_type(self, node: FloatType):
        self._print_indent(f"FloatType at {node.position}, Value: {node.value}")

    def visit_variant_type(self, node: VariantType):
        self._print_indent(f"VariantType at {node.position}, Value: {node.value}")

    def visit_void_type(self, node: VoidType):
        self._print_indent(f"VoidType at {node.position}, Value: {node.value}")

    def visit_any_type(self, node: AnyType):
        self._print_indent(f"AnyType at {node.position}, Value: {node.value}")

    def visit_dictionary_type(self, node: DictionaryType):
        self._print_indent(f"DictionaryType at {node.position}, Value: {node.value}")


    