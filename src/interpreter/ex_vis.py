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
            if function.name in self.functions:
                raise InterpreterError(f"Funkcja {function.name} jest juz zdefiniowana.")
            self.add_function(function.name, function)

        if 'main' not in self.functions:
            raise MainFunctionRequired()
        
        # main_function = self.functions['main']
        # contains_return = any(isinstance(stmt, ReturnStatement) for stmt in main_function.block.statements)
        # if not contains_return:
        #     raise ReturnInMainFunctionRequired


    def visit_function_definition(self, element: FunctionDefintion):
        for param in element.parameters:
            param.accept(self)
        
        if element.name == "main":
            contains_return = any(isinstance(stmt, ReturnStatement) for stmt in element.block.statements)
            if not contains_return:
                raise InterpreterError("Funkcja 'main' musi zawierać instrukcję 'return'.")

        element.block.accept(self)


    def visit_function_arguments(self, element):
        for arg in element:
            arg.accept(self)


    def visit_return_statement(self, element: ReturnStatement):
        if element.expr is not None:
            element.expr.accept(self)
        self.return_flag = True

    def visit_identifier(self, element: Identifier):
        self.last_result = self.context.get_variable_value(element.name)
        self.last_result_type = self.context.get_variable_type(element.name)
        

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

    # def visit_type_expression(self, element: TypeExpression):
    #     # Visit the factor
    #     element.factor.accept(self)
    #     factor_value = self.last_result

    #     if element.factor.name:
    #         factor_value = self.context.get_variable(element.factor.type)
    #     # If a type is provided, check compatibility
    #     if element.type:
    #         element.type.accept(self)
    #         type_value = self.last_result

    #         # Check if the factor matches the type
    #         if not self._check_type_compatibility(factor_value, type_value):
    #             raise TypeMismatchError(f"Wartość '{factor_value}' nie pasuje do typu '{type_value}'.")

    #     self.last_result = factor_value

    def visit_type_expression(self, element: TypeExpression):
        """
        Realizuje wyrażenia w stylu: 
        - 3 is int
        - a is int
        Zwraca True lub False, w zależności od tego, 
        czy 'factor' pasuje do 'type' (jeśli 'type' istnieje).
        """

        # Sprawdzamy, czy factor jest identyfikatorem (np. a is int)
        if isinstance(element.factor, Identifier):
            var_name = element.factor.name
            # Pobieramy z kontekstu **zadeklarowany** typ zmiennej (np. IntegerType)
            declared_type = self.context.get_variable_type(var_name)

            # Czy po "is" rzeczywiście wystąpił jakiś typ do porównania?
            if element.type:
                # Odwiedzamy węzeł z typem (np. IntegerType)
                element.type.accept(self)
                expected_type = self.last_result  # np. instancja IntegerType

                # Porównujemy obiekty typów przez `type(...)` (lub inną metodę, jeśli wolisz)
                self.last_result = (declared_type == expected_type)
            else:
                # Brak typu po 'is' – możesz zwrócić np. sam zadeklarowany typ
                # albo True/False w zależności od wymagań języka
                self.last_result = declared_type

        # Jeśli factor to nie identyfikator (np. literal "3", "hello", wyrażenie itp.)
        else:
            element.factor.accept(self)
            factor_value = self.last_result

            if element.type:
                element.type.accept(self)
                type_value = self.last_result  # np. IntegerType, FloatType, itd.

                # Zamiast rzucać błąd, zwracamy True/False
                self.last_result = self._check_type_compatibility(factor_value, type_value)
            else:
                # Jeśli nie ma typu po 'is', zwróć samą wartość
                self.last_result = factor_value



    def _check_type_compatibility(self, value, type_str):
        """
        Sprawdza, czy runtime'owa wartość `value` jest zgodna z zadanym łańcuchem `type_str`.
        """
        if type_str == "int":
            return isinstance(value, int)
        elif type_str == "float":
            return isinstance(value, float)
        elif type_str == "bool":
            return isinstance(value, bool)
        elif type_str == "string":
            return isinstance(value, str)
        else:
            # Jeśli trafi się coś spoza tych typów, domyślnie False
            return False

    # def visit_negation(self, element: Negation):
    #     element.node.accept(self)
    #     if element.negation_type == "logic" and isinstance(self.last_result, bool):
    #         self.last_result = not self.last_result
    #     elif element.negation_type == "arithmetic" and isinstance(self.last_result, (int, float)):
    #         self.last_result = - self.last_result
    #     else:
    #         raise NegationError(element.position,element.negation_type, self.last_result)

    def visit_negation(self, element: Negation):
        element.node.accept(self)
        if element.negation_type == "logic":
            self.last_result = not self.last_result
        elif element.negation_type == "arithmetic":
            self.last_result = - self.last_result
        else:
            raise NegationError(element.position,element.negation_type, self.last_result)

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

    def visit_relational_operation(self, element: RelationalExpression):
        element.left.accept(self)
        left = self.last_result
        element.right.accept(self)
        right = self.last_result
        self.last_result = left == right

    def visit_not_equal_operation(self, element: NotEqualOperation):
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


    def visit_assignment(self, element: Assignment): # narazie pisze to tak jakbym uwzględniał ze target w assignmencie to raczej identifier alo function.call, tam jeszcze jest obectacces który ma liste ale na tym skupie sie potem
        value = None
        if element.value:
            element.value.accept(self)
        value = self.last_result

        variable_name = element.target.name
        variable_type = element.target.type.value
        # if element.target.name not in self.context.variables:
        #     raise NameError(f"Zmienna '{element.name}' nie została zadeklarowana.")
        
        if variable_name in self.context.variables:
        # Zmienna istnieje -> używamy set_variable
            self.context.set_variable(variable_name, value)
        else:
        # Zmienna nie istnieje -> dodajemy do kontekstu
            self.context.add_variable(variable_name, value, variable_type)


    def visit_type_match(self, element: TypeMatch):
        """
        match expression [as x] {
            type => { ... }
            null => { ... }
            _    => { ... }
        }

        1. Odwiedzamy expression, co ustawia:
        self.last_result      = wartość wyrażenia  (np. 42, "hello", None, ...)
        self.last_result_type = typ wyrażenia      (np. "int", "string", "null", ...)
        2. Jeśli jest 'as x', zapisujemy do kontekstu oryginalną wartość wyrażenia.
        3. Iterujemy po case'ach i sprawdzamy dopasowanie na podstawie expr_type.
        """
        # 1. Obliczamy wyrażenie
        element.expression.accept(self)
        expr_value = self.last_result
        expr_type = self.last_result_type  # np. "int", "float", "string", "null", ...

        # 2. Jeśli jest 'as x', zapisujemy expr_value pod nazwą x (opcjonalnie także typ)
        if element.identifier:
            var_name = element.identifier
            if self.context.has_variable(var_name):
                self.context.set_variable_value(var_name, expr_value)
            else:
                # Możesz też podać var_type=expr_type, jeśli chcesz przechowywać deklarowany typ.
                self.context.add_variable(var_name, expr_value, var_type=None)

        # 3. Sprawdzamy kolejno case'y
        for case in element.cases:
            # Wywołujemy funkcję pomocniczą i przekazujemy expr_type (nie wartość!)
            if self.visit_match_case(case, expr_type):
                # Pierwszy dopasowany case wykonuje swój blok
                break

        # Nie nadpisujemy self.last_result - 
        # bo np. wewnątrz case mogło być 'return', czy inne działania.
        # Zostawiamy interpretację w takim stanie, w jakim się zakończyła.



    def visit_match_case(self, case: MatchCase, expr_type: str):
        """
        Sprawdza, czy expr_type (np. "int", "float", "null", "string", ...)
        pasuje do `case.type`, który może być:
        - VoidType z value="null"
        - AnyType z value="_"
        - Normalnym typem (IntegerType, FloatType itp.)
        
        Jeśli pasuje, wywołuje block i zwraca True.
        W przeciwnym razie zwraca False.
        """

        match_case_type = case.type

        # 1. null-case (np. 'null' => {...})
        if isinstance(match_case_type, VoidType) and match_case_type.value == "null":
            if expr_type == "null":
                # Dopasowanie się udało, wizytujemy block
                case.block.accept(self)
                return True
            return False

        # 2. underscore-case ('_' => {...})
        if isinstance(match_case_type, AnyType) and match_case_type.value == "_":
            # '_' pasuje do wszystkiego
            case.block.accept(self)
            return True

        # 3. normalny typ (np. IntegerType, FloatType, StringType...)
        #    Odwiedzamy, żeby w self.last_result dostać np. "int", "float"
        match_case_type.accept(self)
        expected_type_str = self.last_result  # np. "int", "float", ...

        # Porównujemy expr_type z expected_type_str
        if expr_type == expected_type_str:
            case.block.accept(self)
            return True

        # Jeśli nie pasuje, zwracamy False
        return False


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
        new_context = Context()

        # Przypisujemy argumenty do parametrów w nowym kontekście
        for param, value in zip(function.parameters, evaluated_arguments):
            if param.type is not None:
                if not self._check_type_compatibility(value, param.type.value):
                    raise TypeMismatchError(
                f"Argument '{param.name}' nie pasuje do typu {param.type} "
                f"(wartość = {value})."
            )

    # Dodajemy zmienną do kontekstu, przekazując również typ
                new_context.add_variable(param.name, value, param.type)

        # Dodajemy nowy kontekst na stos
        self.context_stack.append(new_context)
        self.context = new_context

        try:
            # Wizytujemy ciało funkcji
            function.block.accept(self)

            # Wynik funkcji to self.last_result (ustawiane przez `return`)
            result = self.last_result

        finally:
            # Usuwamy bieżący kontekst i przywracamy poprzedni
            self.context_stack.pop()
            self.context = self.context_stack[-1]

        # Zwracamy wynik funkcji
        self.last_result = result


    def visit_object_access(self, element):
        pass

    def visit_block(self, element: Block):
        for statement in element.statements:
            statement.accept(self)
            if self.return_flag:
                break

    def visit_string_type(self, element: StringType):
        self.last_result = element.value

    def visit_integer_type(self, element: IntegerType):
        self.last_result = element.value

    def visit_bool_type(self, element: BoolType):
        self.last_result = element.value

    def visit_float_type(self, element: FloatType):
        self.last_result = element.value

    def visit_variant_type(self, element: VariantType):
        self.last_result = element.value

    def visit_void_type(self, element: VoidType):
        self.last_result = element.value

    def visit_any_type(self, element: AnyType):
        self.last_result = element.value

    def visit_dictionary_type(self, element: DictionaryType):
        self.last_result = element.value
