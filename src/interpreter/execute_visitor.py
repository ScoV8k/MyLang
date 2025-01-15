from src.parser.objects import *
from src.interpreter.interpreter import Context
from src.errors.interpreter_errors import *
import numpy as np
import numbers
import sys, os
from src.interpreter.functions import built_in_functions
from src.interpreter.variable import VarType
from src.interpreter.typed_value import TypedValue



class ExecuteVisitor(Visitor):
    def __init__(self, recursion_limit=100):
        super().__init__()
        self.functions = built_in_functions.copy()
        self.last_result = None
        self.return_flag = None
        self.context_stack = [Context()]
        self.context = self.context_stack[-1]
        self.additional_args = None
        self.temp_object = None
        self.break_flag = False
        self.return_value = None

        self.TYPE_MAPPING = {
            IntegerType: VarType.INT, 
            FloatType: VarType.FLOAT,      
            BoolType: VarType.BOOL,         
            StringType: VarType.STRING,      
            DictionaryType: VarType.DICT,   
            VariantType: VarType.VARIANT,
            VoidType: VarType.NULL
            }
        
        self.VALUE_TYPE_MAPPING = {
            int: VarType.INT,
            float: VarType.FLOAT,
            bool: VarType.BOOL,
            str: VarType.STRING,
            dict: VarType.DICT,
            
        }
            
    def map_object_type_to_vartype(self, parser_type):
        result = self.TYPE_MAPPING.get(type(parser_type))
        return result
    

    def map_value_type_to_vartype(self, value):
        result = self.VALUE_TYPE_MAPPING.get(type(value), VarType.NULL)
        return result
    
    def add_function(self, name, func):
        self.functions[name] = func


    def visit_program(self, element: Program):
        for function in element.functions:
            if function.name in self.functions:
                raise InterpreterError(f"Funkcja {function.name} jest juz zdefiniowana.")
            self.add_function(function.name, function)

        if 'main' not in self.functions:
            raise MainFunctionRequired()
        
        main_call = FunctionCall(self.functions.get('main').position, 'main', [])
        main_call.accept(self) # wewnątrz wizytacji programu te 2 linijki ta i wyzej
        
        # main_function = self.functions['main']
        # contains_return = any(isinstance(stmt, ReturnStatement) for stmt in main_function.block.statements)
        # if not contains_return:
        #     raise ReturnInMainFunctionRequired


    def visit_function_definition(self, element: FunctionDefintion):
        for param in element.parameters:
            param.accept(self)
        
        # if element.name == "main":
        #     contains_return = any(isinstance(stmt, ReturnStatement) for stmt in element.block.statements)
        #     if not contains_return:
        #         raise InterpreterError("Funkcja 'main' musi zawierać instrukcję 'return'.")

        element.block.accept(self)
        # weryfikacja flagi return i typu funkcji bo void nie ma inne maja i reset flagi return



    def visit_function_arguments(self, element):
        for arg in element:
            arg.accept(self)


    def visit_return_statement(self, element: ReturnStatement):
        if element.expr is not None:
            element.expr.accept(self)
        self.return_flag = True
        self.return_value = self.last_result

    def visit_identifier(self, element: Identifier):
        self.last_result = self.context.get_variable(element.name)
        self.last_result_type = self.context.get_variable_type(element.name)
        

    def visit_parameter(self, element):
        var_type = self.map_object_type_to_vartype(element.type)
        self.context.add_variable(element.name, None, var_type)

    def visit_if_statement(self, element: IfStatement):
        element.condition.accept(self)
        if self.last_result.value:
            element.statements.accept(self)
        elif element.else_statement:
            element.else_statement.accept(self)


    def visit_while_statement(self, element: WhileStatement):
        self.context.while_flag += 1
        element.condition.accept(self)
        while self.last_result:
            self.context.reset_flags()
            element.condition.accept(self)
            if not self.last_result.value or self.break_flag:
                break
            element.statements.accept(self)
            if self.return_flag or self.break_flag:
                break
        self.context.while_flag -= 1
        self.break_flag = False


    def visit_for_each_statement(self, element: ForEachStatement):
        element.struct.accept(self)

        dict_value = self.last_result  
        if dict_value.type != VarType.DICT:
            raise InterpreterError(
                f"Pętla 'for each' wymaga słownika, otrzymano typ: {dict_value.type}."
            )
        for current_key, current_value in dict_value.value.items():
            self.context.set_variable(element.key, current_key)
            self.context.set_variable(element.value, current_value)
            element.statements.accept(self)
            if self.break_flag or self.return_flag:
                break
        self.break_flag = False


    def visit_or_expression(self, element: OrExpression):
        for expr in element.expressions:
            expr.accept(self)
            if self.last_result.value: 
                self.last_result.value = True
                return
        self.last_result.value = False


    def visit_and_expression(self, element: AndExpression):
        for expr in element.expressions:
            expr.accept(self) 
            if not self.last_result.value:
                self.last_result.value = False
                return
        self.last_result.value = True

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
        if isinstance(element.factor, Identifier):
            var_name = element.factor.name
            variable = self.context.get_variable(var_name)
            if element.type:

                self.last_result = TypedValue((variable.type == self.map_object_type_to_vartype(element.type)), VarType.BOOL)
            else:
                self.last_result = variable.type # nie wiem co dokładnie tutaj abc is (i tu nic nie ma?)

        else:
            element.factor.accept(self)
            factor_value = self.last_result

            if element.type:
                # element.type.accept(self)
                self.last_result = TypedValue(self._check_type_compatibility(factor_value, element.type), VarType.BOOL)
            else:
                self.last_result = factor_value # tez chyba nie mozliwe



    def _check_type_compatibility(self, value, type_str):
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
            # self.last_result = not self.last_result
            self.last_result.set_value(not self.last_result.value)
        elif element.negation_type == "arithmetic":
            # self.last_result = - self.last_result
            self.last_result.set_value(- self.last_result.value)
        else:
            raise NegationError(element.position,element.negation_type, self.last_result)

    def visit_sum_expression(self, element: SumExpression):
        element.left.accept(self)
        left_value = self.last_result
        if not isinstance(left_value.value, (int, float)):
            raise TypeError(f"Lewy operand '+' musi być liczbą, otrzymano: {type(left_value.value).__name__}.")
        element.right.accept(self)
        right_value = self.last_result
        if not isinstance(right_value.value, (int, float)):
            raise TypeError(f"Prawy operand '+' musi być liczbą, otrzymano: {type(right_value.value).__name__}.")

        result_value = left_value.value + right_value.value

        if left_value.type == VarType.FLOAT or right_value.type == VarType.FLOAT:
            result_type = VarType.FLOAT
        else:
            result_type = VarType.INT

        self.last_result = TypedValue(result_value, result_type)

    def visit_sub_expression(self, element: SubExpression):
        # 1. Odwiedzamy lewe wyrażenie
        element.left.accept(self)
        left_var = self.last_result  # to jest Variable
        if not isinstance(left_var.value, (int, float)):
            raise TypeError(
                f"Lewy operand '-' musi być liczbą, otrzymano: {type(left_var.value).__name__}."
            )
        
        element.right.accept(self)
        right_var = self.last_result
        if not isinstance(right_var.value, (int, float)):
            raise TypeError(
                f"Prawy operand '-' musi być liczbą, otrzymano: {type(right_var.value).__name__}."
            )

        result_value = left_var.value - right_var.value
        
        if left_var.type == VarType.FLOAT or right_var.type == VarType.FLOAT:
            result_type = VarType.FLOAT
        else:
            result_type = VarType.INT

        self.last_result = TypedValue(result_value, result_type)


    def visit_mul_expression(self, element: MulExpression):
        element.left.accept(self)
        left_var = self.last_result
        left_value = left_var.value
        
        element.right.accept(self)
        right_var = self.last_result
        right_value = right_var.value

        if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
            result_value = left_value * right_value
            # wynik jest float, jeśli któryś operand to float
            if left_var.type == VarType.FLOAT or right_var.type == VarType.FLOAT:
                result_type = VarType.FLOAT
            else:
                result_type = VarType.INT

        elif isinstance(left_value, str) and isinstance(right_value, int):
            result_value = left_value * right_value
            result_type = VarType.STRING

        elif isinstance(right_value, str) and isinstance(left_value, int):
            result_value = right_value * left_value
            result_type = VarType.STRING

        else:
            raise TypeError(
                f"Nieobsługiwane typy operandów dla '*': "
                f"{type(left_value).__name__} i {type(right_value).__name__}."
            )

        self.last_result = TypedValue(result_value, result_type)



    def visit_div_expression(self, element: DivExpression):
        element.left.accept(self)
        left_var = self.last_result
        element.right.accept(self)
        right_var = self.last_result
        
        if not isinstance(left_var.value, (int, float)):
            raise TypeError(f"Lewy operand '/' musi być liczbą, otrzymano: {type(left_var.value).__name__}.")
        if not isinstance(right_var.value, (int, float)):
            raise TypeError(f"Prawy operand '/' musi być liczbą, otrzymano: {type(right_var.value).__name__}.")
        if right_var.value == 0:
            raise ZeroDivisionError("Dzielenie przez zero jest niedozwolone.")
        result_value = left_var.value / right_var.value
        if left_var.type == VarType.FLOAT or right_var.type == VarType.FLOAT:
            result_type = VarType.FLOAT
        else:
            result_type = VarType.INT
        self.last_result = TypedValue(result_value, result_type)

    def visit_break_statement(self, element: BreakStatement) :
        if self.context.while_flag == 0:
            raise RuntimeError(f"Break statement used outside of while loop at position: {element.position}")
        self.break_flag = True
        return

    def visit_equality_operation(self, element: EqualityOperation):
        element.left.accept(self)
        left_var = self.last_result
        element.right.accept(self)
        right_var = self.last_result
        result_value = (left_var.value == right_var.value)
        self.last_result = TypedValue(result_value, VarType.BOOL)

    def visit_relational_operation(self, element: RelationalExpression):
        element.left.accept(self)
        left_var = self.last_result
        element.right.accept(self)
        right_var = self.last_result
        result_value = (left_var.value == right_var.value)
        self.last_result = TypedValue(result_value, VarType.BOOL)

    def visit_not_equal_operation(self, element: NotEqualOperation):
        element.left.accept(self)
        left_var = self.last_result
        element.right.accept(self)
        right_var = self.last_result
        result_value = (left_var.value != right_var.value)
        self.last_result = TypedValue(result_value, VarType.BOOL)

    def visit_greater_operation(self, element: GreaterOperation):
        element.left.accept(self)
        left_var = self.last_result
        element.right.accept(self)
        right_var = self.last_result
        result_value = (left_var.value > right_var.value)
        self.last_result = TypedValue(result_value, VarType.BOOL)

    def visit_greater_equal_operation(self, element: GreaterEqualOperation):
        element.left.accept(self)
        left_var = self.last_result
        element.right.accept(self)
        right_var = self.last_result
        result_value = (left_var.value >= right_var.value)
        self.last_result = TypedValue(result_value, VarType.BOOL)

    def visit_less_operation(self, element: LessOperation):
        element.left.accept(self)
        left_var = self.last_result
        element.right.accept(self)
        right_var = self.last_result
        result_value = (left_var.value < right_var.value)
        self.last_result = TypedValue(result_value, VarType.BOOL)

    def visit_less_equal_operation(self, element: LessEqualOperation):
        element.left.accept(self)
        left_var = self.last_result
        element.right.accept(self)
        right_var = self.last_result
        result_value = (left_var.value <= right_var.value)
        self.last_result = TypedValue(result_value, VarType.BOOL)


    def visit_bool_value(self, element: BoolValue):
        # self.last_result = element.value
        self.last_result = TypedValue(element.value, VarType.BOOL)

    def visit_integer_value(self, element: IntegerValue):
        # self.last_result = element.value
        self.last_result = TypedValue(element.value, VarType.INT)
        # self.last_result = 1

    def visit_float_value(self, element: FloatValue):
        # self.last_result = element.value
        self.last_result = TypedValue(element.value, VarType.FLOAT)

    def visit_string_value(self, element: StringValue):
        self.last_result = TypedValue(element.value, VarType.STRING)

    def visit_null_value(self, element: NullValue):
        self.last_result = TypedValue(element.value, VarType.NULL)


    def visit_dictionary(self, element: Dictionary):
        dictionary_result = {}
        for entry in element.dictionary_entries:
            entry.accept(self)
            key, value = self.last_result
            # if key in dictionary_result:
            #     raise KeyError(f"Klucz '{key}' został już zdefiniowany w słowniku.")
            dictionary_result[key] = value
        self.last_result = dictionary_result


    def visit_dictionary_entry(self, element: DictionaryEntry):
        element.expr1.accept(self)
        key = self.last_result
        element.expr2.accept(self)
        value = self.last_result 
        self.last_result = (key, value)

    def visit_declaration(self, element: Declaration):

        variable_name = element.target.name

        if self.context.has_variable(variable_name):
            raise DeclarationError(variable_name)
        variable_type = self.map_object_type_to_vartype(element.target.type)

        value = None
        if element.value is not None:
            element.value.accept(self)
            value = self.last_result
        else:
            # Jeśli nie ma przypisania, można np. ustawić domyślne Null
            value = TypedValue(None, VarType.NULL)

        # 5. (opcjonalnie) sprawdzamy kompatybilność typów, np.:
        # if value.type != variable_type and variable_type != VarType.VARIANT:
        #     raise TypeMismatchError(
        #         f"Próbowano zadeklarować zmienną typu {variable_type.name}, "
        #         f"ale wyrażenie ma typ {value.type.name}."
        #     )

        # 6. Dodajemy zmienną do kontekstu (w zależności od struktury danych w Context)
        #    - Możesz np. trzymać tam TypedValue, albo osobno value i typ.
        if variable_type == VarType.DICT:
            # Jeżeli chcesz przechowywać cały TypedValue
            self.context.add_variable(variable_name, value, variable_type)
        else:
            # Jeżeli chcesz przechowywać tylko “surową” wartość, a typ osobno
            self.context.add_variable(variable_name, value.value, variable_type)


    # def visit_assignment(self, element: Assignment):
    #     """
    #     assignment ::= obj_access, [ "=", expression ], ";" ;
    #     Logika:
    #     1. Sprawdź, czy zmienna już istnieje w kontekście:
    #         - Jeśli nie istnieje, rzuć błąd.
    #     2. Odwiedź wyrażenie (element.value), aby uzyskać wartość do przypisania.
    #     3. Opcjonalnie sprawdź kompatybilność typów z już istniejącym typem zmiennej.
    #     4. Ustaw wartość w kontekście.
    #     """

    #     # 1. Pobieramy nazwę zmiennej, do której przypisujemy
    #     variable_name = element.target.name

    #     # Sprawdzamy, czy zmienna istnieje
    #     if not self.context.has_variable(variable_name):
    #         raise NameError(f"Zmienna '{variable_name}' nie została zadeklarowana przed użyciem.")

    #     # 2. Wywołujemy wyrażenie po "=" (jeśli jest), żeby wyliczyć wartość
    #     if element.value is not None:
    #         element.value.accept(self)
    #         value = self.last_result
    #     else:
    #         # Jeśli assignment może być bez wartości, ustaw np. None
    #         # (zwykle w normalnej gramatyce assignment = ...) jest wartość, ale to zależy od języka
    #         value = TypedValue(None, VarType.NULL)

    #     # 3. (opcjonalnie) sprawdzamy, czy typ jest zgodny z typem zmiennej w kontekście
    #     existing_var = self.context.get_variable_typed(variable_name)  # Załóżmy, że get_variable_typed zwraca TypedValue
    #     if existing_var.type != value.type and existing_var.type != VarType.VARIANT:
    #         # Możesz zdecydować, czy rzutować, czy rzucić błąd
    #         raise TypeMismatchError(
    #             f"Niezgodność typów w przypisaniu do '{variable_name}'. "
    #             f"Oczekiwany: {existing_var.type}, otrzymany: {value.type}."
    #         )

    #     # 4. Ustawiamy nową wartość w kontekście
    #     if value.type == VarType.DICT:
    #         self.context.set_variable(variable_name, value)  # lub value.value, zależy jak przechowujesz
    #     else:
    #         self.context.set_variable(variable_name, value.value)

    # assignment ::= obj_access, [ "=", expression ], ";" ;
    def visit_assignment(self, element: Assignment):
        value = None
        if element.value:
            element.value.accept(self)
        value = self.last_result

        variable_name = element.target.name
        # if type(element.target) == Identifier: # TUTAJ !!!!!!!!!!!!!!
        #     variable_type = self.context.get_variable_type(variable_name)
        # else:
        #     variable_type = self.map_object_type_to_vartype(element.target.type)


        # variable_type = self.map_object_type_to_vartype(element.target.type)
        # # if element.target.name not in self.context.variables:
        # #     raise NameError(f"Zmienna '{element.name}' nie została zadeklarowana.")
        
        # value_to_set = value if variable_type == VarType.DICT else value.value
        value_to_set = value.value
        if variable_name in self.context.variables:
            self.context.set_variable(variable_name, value_to_set)
        else:
            self.context.add_variable(variable_name, value_to_set, variable_type)

    # # declaration ::= parameter, [ "=", expression ], ";" ;
    # def visit_declaration(self, element: Declaration):
    #     value = None
    #     if element.value:
    #         element.value.accept(self)
    #     value = self.last_result

    #     variable_name = element.target.name
    #     # if type(element.target) == Identifier: # TUTAJ !!!!!!!!!!!!!!
    #     #     variable_type = self.context.get_variable_type(variable_name)
    #     # else:
    #     #     variable_type = self.map_object_type_to_vartype(element.target.type)


    #     variable_type = self.map_object_type_to_vartype(element.target.type)
    #     # if element.target.name not in self.context.variables:
    #     #     raise NameError(f"Zmienna '{element.name}' nie została zadeklarowana.")
        
    #     value_to_set = value if variable_type == VarType.DICT else value.value

    #     if variable_name in self.context.variables:
    #         self.context.set_variable(variable_name, value_to_set)
    #     else:
    #         self.context.add_variable(variable_name, value_to_set, variable_type)



    def visit_type_match(self, element: TypeMatch):

        element.expression.accept(self)
        expr_value = self.last_result  

        if element.identifier:
            var_name = element.identifier
            if self.context.has_variable(var_name):
                self.context.set_variable(var_name, expr_value)
            else:

                self.context.add_variable(var_name, expr_value.value, expr_value.type)

        for case in element.cases:

            if self.visit_match_case(case, expr_value):
                break


    def visit_match_case(self, case: MatchCase, expr_value):

        match_case_type = case.type
            
        # if isinstance(match_case_type, VoidType) and match_case_type.value == "null":
        #     if expr_value.type == VarType.VARIANT:
        #         case.block.accept(self)
        #         return True
        #     return False

        # if isinstance(match_case_type, AnyType) and match_case_type.value == "_":
        #     # '_' pasuje do wszystkiego
        #     case.block.accept(self)
        #     return True


        # # match_case_type.accept(self)

        # if expr_value.type == self.map_object_type_to_vartype(match_case_type):
        #     case.block.accept(self)
        #     return True
        # return False

        if isinstance(match_case_type, AnyType) and match_case_type.value == "_":
            # '_' pasuje do wszystkiego
            case.block.accept(self)
            return True
        
        if self.map_value_type_to_vartype(expr_value.value) == self.map_object_type_to_vartype(match_case_type):
            case.block.accept(self)
            return True
        return False


    def visit_function_call(self, element: FunctionCall):
        if element.function_name not in self.functions:
            raise NameError(f"Funkcja '{element.function_name}' nie została zadeklarowana.")
        # coś w tym miejscu powiedział e ma być get powyej bo 2 razy robie potem z tym co jest ponizej function =
        #     tak jak to ma być ->  if (type := self.TYPE_MAPPING.get(self.current_token.type)):
        function = self.functions[element.function_name]

        evaluated_arguments = []
        for argument in element.arguments:
            argument.accept(self)  
            evaluated_arguments.append(self.last_result) 
        
        if element.function_name != 'print':
            self.additional_args = [self.temp_object] + evaluated_arguments
        else:
            self.additional_args = evaluated_arguments

        new_context = Context()

        if type(function) == FunctionDefintion:
            if (len(evaluated_arguments) != len(function.parameters)) and type(function) == FunctionCall:
                raise TypeError(
                    f"Funkcja '{element.function_name}' oczekuje {len(function.parameters)} argumentów, "
                    f"otrzymano {len(evaluated_arguments)}."
                )

            # new_context = Context()

            for param, value in zip(function.parameters, evaluated_arguments):
                if param.type is not None:
                    if not self._check_type_compatibility(value.value, param.type.value): # tu dodałem value.value
                        raise TypeMismatchError(
                    f"Argument '{param.name}' nie pasuje do typu {param.type} "
                    f"(wartość = {value})."
                )

                    new_context.add_variable(param.name, value.value, self.map_object_type_to_vartype(param.type))

        self.context_stack.append(new_context)
        self.context = new_context

        try:
            function.block.accept(self)
            self.return_flag = None
            result = self.last_result

        finally:
            self.context_stack.pop()
            self.context = self.context_stack[-1]

        # Zwracamy wynik funkcji
        self.last_result = result



    def visit_object_access(self, element: ObjectAccess):
        """
        Obsługa wyrażeń typu a.add("key", "value") itp.
        element.items to lista, której pierwszy element powinien być identyfikatorem
        (np. 'a'), a kolejne to np. functionCall (np. add("key", "value")).
        """

        # 1. Najpierw odwiedzamy pierwszy element (bazowy identyfikator).
        #    Zakładamy, że jest to np. 'a' (Identifier).
        base_item = element.items[0]
        base_item.accept(self)
        current_object = self.last_result  # np. tutaj mamy TypedValue(dict, VarType.DICT)

        # 2. Przechodzimy przez kolejne elementy w element.items.
        #    Mogą to być identyfikatory (dostęp do atrybutu) lub FunctionCall (wywołanie metody).
        for item in element.items[1:]:
            if isinstance(item, Identifier):
                # Jeśli chcemy pozwolić na dostęp do atrybutów obiektu (np. a.xyz),
                # można tu obsłużyć np. current_object = current_object.value[item.name]
                # W zależności od tego, czy chcemy w ogóle takie konstrukcje obsługiwać.
                # Dla prostoty pominiemy na razie tę część.
                pass

            elif isinstance(item, FunctionCall):
                self.temp_object = current_object
                item.accept(self)

        self.last_result = current_object


    def visit_block(self, element: Block):
        for statement in element.statements:
            statement.accept(self)
            if self.return_flag or self.break_flag:
                break

    def visit_string_type(self, element: StringType):
        self.last_result = self.map_object_type_to_vartype(element)

    def visit_integer_type(self, element: IntegerType):
        self.last_result = self.map_object_type_to_vartype(element)

    def visit_bool_type(self, element: BoolType):
        self.last_result = self.map_object_type_to_vartype(element)

    def visit_float_type(self, element: FloatType):
        self.last_result = self.map_object_type_to_vartype(element)

    def visit_variant_type(self, element: VariantType):
        self.last_result = self.map_object_type_to_vartype(element)

    def visit_void_type(self, element: VoidType):
        self.last_result = self.map_object_type_to_vartype(element)

    def visit_any_type(self, element: AnyType):
        self.last_result = self.map_object_type_to_vartype(element)

    def visit_dictionary_type(self, element: DictionaryType):
        self.last_result = self.map_object_type_to_vartype(element)

    def visit_built_in_function(self, element):
        args = self.additional_args
        res =  element.function(*args)
        self.last_result = res


#  Przemyślenia: podobno mona wywalić te wizytacje typów, ale moge
# je zostawić i zwracać w nich wartość moją np VarType.INT

# jestem w trakcie zmieniania tych typów, mój pomysł jest taki eby i visit_int_type zwracało variable

# Na przykładzie sum expression moe być zwrócony albo iden albo value
# dlatego visit_int_value musi zwracac variable i ident te zwróci variable


#zmienilem naraxie tylko sum_expr:         left_value = self.last_result.value i 