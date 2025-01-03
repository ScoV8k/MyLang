from src.parser.objects import *
from src.interpreter.interpreter import Context
from src.errors.interpreter_errors import *
import numpy as np
import numbers
import sys, os
from src.interpreter.functions import ImportedObject, built_in_functions



class ExecuteVisitor(Visitor):
    def __init__(self, recursion_limit=100):
        super().__init__()
        self.functions = built_in_functions.copy()
        self.last_result = None
        self.return_flag = None
        self.context_stack = [Context()]
        self.context = self.context_stack[-1]
    
    def add_function(self, name, func):
        self.functions[name] = func


    def visit_program(self, element: Program):
        for function in element.functions:
            self.add_function(function.name, function)


    def visit_function_definition(self, element):
        pass


    def visit_function_arguments(self, element):
        for arg in element:
            arg.accept(self)


    def visit_return_statement(self, element: ReturnStatement):
        if element.expr is not None:
            element.expr.accept(self)
        self.return_flag = True

    def visit_identifier(self, element: Identifier):
        self.last_result = self.context.get_variable(element.name)

    def visit_parameter(self, element):
        pass

    def visit_if_statement(self, element: IfStatement):
        element.condition.accept(self)
        if self.last_result:
            element.statements.accept(self)
        elif element.else_statement:
            element.else_statement.accept(self)


    def visit_while_statement(self, element: WhileStatement):
        self.context.while_flag += 1
        element.condition.accept(self)
        while self.last_result:
            self.context.reset_flags()
            element.condition.accept(self)
            if not self.last_result:
                break
            element.statements.accept(self)
            if self.return_flag:
                break
        self.context.while_flag -= 1

    def visit_for_each_statement(self, element):
        pass

    def visit_or_expression(self, element: OrExpression):
        for expr in element.expressions:
            expr.accept(self)
            if self.last_result: 
                self.last_result = True
                return
        self.last_result = False


    def visit_and_expression(self, element: AndExpression):
        for expr in element.expressions:
            expr.accept(self) 
            if not self.last_result:
                self.last_result = False
                return
        self.last_result = True

    def visit_type_expression(self, element: TypeExpression):
        pass

    def visit_negation(self, element):
        pass

    def visit_sum_expression(self, element: SumExpression):
        element.left.accept(self)
        left_value = self.last_result
        if not isinstance(left_value, (int, float)):
            raise TypeError(f"Lewy operand '+' musi być liczbą, otrzymano: {type(left_value).__name__}.")
        element.right.accept(self)
        right_value = self.last_result
        if not isinstance(right_value, (int, float)):
            raise TypeError(f"Prawy operand '+' musi być liczbą, otrzymano: {type(right_value).__name__}.")

        self.last_result = left_value + right_value

    def visit_sub_expression(self, element: SubExpression):
        element.left.accept(self)
        left_value = self.last_result
        if not isinstance(left_value, (int, float)):
            raise TypeError(f"Lewy operand '-' musi być liczbą, otrzymano: {type(left_value).__name__}.")
        element.right.accept(self)
        right_value = self.last_result
        if not isinstance(right_value, (int, float)):
            raise TypeError(f"Prawy operand '-' musi być liczbą, otrzymano: {type(right_value).__name__}.")
        self.last_result = left_value - right_value

    def visit_mul_expression(self, element: MulExpression):
        element.left.accept(self)
        left_value = self.last_result
        element.right.accept(self)
        right_value = self.last_result

        if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
            self.last_result = left_value * right_value
        elif isinstance(left_value, str) and isinstance(right_value, int):
            self.last_result = left_value * right_value
        elif isinstance(right_value, str) and isinstance(left_value, int):
            self.last_result = right_value * left_value
        else:
            raise TypeError(
                f"Nieobsługiwane typy operandów dla '*': {type(left_value).__name__} i {type(right_value).__name__}."
            )


    def visit_div_expression(self, element: DivExpression):
        element.left.accept(self)
        left_value = self.last_result
        if not isinstance(left_value, (int, float)):
            raise TypeError(f"Lewy operand '/' musi być liczbą, otrzymano: {type(left_value).__name__}.")

        element.right.accept(self)
        right_value = self.last_result
        if not isinstance(right_value, (int, float)):
            raise TypeError(f"Prawy operand '/' musi być liczbą, otrzymano: {type(right_value).__name__}.")

        if right_value == 0:
            raise ZeroDivisionError("Dzielenie przez zero jest niedozwolone.")
        
        self.last_result = left_value / right_value


    def visit_equality_operation(self, element: EqualityOperation):
        element.left.accept(self)
        left = self.last_result
        element.right.accept(self)
        right = self.last_result
        self.last_result = left == right

    def visit_relational_operation(self, element):
        pass

    def visit_not_equal_operation(self, element):
        element.left.accept(self)
        left = self.last_result
        element.right.accept(self)
        right = self.last_result
        self.last_result = left != right

    def visit_greater_operation(self, element: GreaterOperation):
        element.left.accept(self)
        left = self.last_result
        element.right.accept(self)
        right = self.last_result
        self.last_result = left > right

    def visit_greater_equal_operation(self, element: GreaterEqualOperation):
        element.left.accept(self)
        left = self.last_result
        element.right.accept(self)
        right = self.last_result
        self.last_result = left >= right

    def visit_less_operation(self, element: LessOperation):
        element.left.accept(self)
        left = self.last_result
        element.right.accept(self)
        right = self.last_result
        self.last_result = left < right

    def visit_less_equal_operation(self, element: LessEqualOperation):
        element.left.accept(self)
        left = self.last_result
        element.right.accept(self)
        right = self.last_result
        self.last_result = left <= right

    def visit_bool_value(self, element: BoolValue):
        self.last_result = element.value

    def visit_integer_value(self, element: IntegerValue):
        self.last_result = element.value

    def visit_float_value(self, element: FloatValue):
        self.last_result = element.value

    def visit_string_value(self, element: StringValue):
        self.last_result = element.value

    def visit_dictionary(self, element: Dictionary):
        dictionary_result = {}
        for entry in element.dictionary_entries:
            entry.accept(self)
            key, value = self.last_result
            if key in dictionary_result:
                raise KeyError(f"Klucz '{key}' został już zdefiniowany w słowniku.")
            dictionary_result[key] = value
        self.last_result = dictionary_result


    def visit_dictionary_entry(self, element: DictionaryEntry):
        element.expr1.accept(self)
        key = self.last_result
        element.expr2.accept(self)
        value = self.last_result 
        self.last_result = (key, value)


    def visit_assignment(self, element: Assignment):
        value = None
        if element.value:
            element.value.accept(self)
        value = self.last_result

        if element.name not in self.context.variables:
            raise NameError(f"Zmienna '{element.name}' nie została zadeklarowana.")
        
        self.context.variables[element.name] = value


    def visit_type_match(self, element):
        pass


    def visit_match_case(self, element):
        pass


    def visit_function_call(self, element: FunctionCall):
        # Sprawdzamy, czy funkcja istnieje w kontekście
        if element.function_name not in self.functions:
            raise NameError(f"Funkcja '{element.function_name}' nie została zadeklarowana.")

        # Pobieramy definicję funkcji
        function = self.functions[element.function_name]

        # Wizytujemy argumenty i zbieramy ich wartości
        evaluated_arguments = []
        for argument in element.arguments:
            argument.accept(self)  # Wizytujemy wyrażenie argumentu
            evaluated_arguments.append(self.last_result)  # Dodajemy wynik do listy argumentów

        # Sprawdzamy zgodność liczby argumentów
        if len(evaluated_arguments) != len(function.parameters):
            raise TypeError(
                f"Funkcja '{element.function_name}' oczekuje {len(function.parameters)} argumentów, "
                f"otrzymano {len(evaluated_arguments)}."
            )

        # Tworzymy nowy kontekst dla funkcji
        new_context = Context(parent=self.context)

        # Przypisujemy argumenty do parametrów w nowym kontekście
        for param, value in zip(function.parameters, evaluated_arguments):
            new_context.set_variable(param.name, value, param.var_type)

        # Zapisujemy bieżący kontekst i przełączamy na nowy
        self.context_stack.append(new_context)
        self.context = new_context

        try:
            # Wizytujemy ciało funkcji
            function.body.accept(self)

            # Wynik funkcji to self.last_result (ustawiane przez `return`)
            result = self.last_result

        finally:
            # Przywracamy poprzedni kontekst
            self.context_stack.pop()
            self.context = self.context_stack[-1]

        # Zwracamy wynik funkcji
        self.last_result = result


    def visit_object_access(self, element):
        pass

    def visit_block(self, element):
        pass

    def visit_string_type(self, element):
        pass

    def visit_integer_type(self, element):
        pass

    def visit_bool_type(self, element):
        pass

    def visit_float_type(self, element):
        pass

    def visit_variant_type(self, element):
        pass

    def visit_void_type(self, element):
        pass

    def visit_any_type(self, element):
        pass

    def visit_dictionary_type(self, element):
        pass
