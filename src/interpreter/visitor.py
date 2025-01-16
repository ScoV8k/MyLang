from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visit_program(self, element):
        pass

    @abstractmethod
    def visit_function_definition(self, element):
        pass

    # @abstractmethod
    # def visit_function_arguments(self, element):
    #     pass

    @abstractmethod
    def visit_return_statement(self, element):
        pass

    @abstractmethod
    def visit_identifier(self, element):
        pass

    @abstractmethod
    def visit_parameter(self, element):
        pass

    @abstractmethod
    def visit_if_statement(self, element):
        pass

    @abstractmethod
    def visit_while_statement(self, element):
        pass

    @abstractmethod
    def visit_for_each_statement(self, element):
        pass

    @abstractmethod
    def visit_or_expression(self, element):
        pass

    @abstractmethod
    def visit_and_expression(self, element):
        pass

    @abstractmethod
    def visit_type_expression(self, element):
        pass

    @abstractmethod
    def visit_negation(self, element):
        pass

    @abstractmethod
    def visit_sum_expression(self, element):
        pass

    @abstractmethod
    def visit_sub_expression(self, element):
        pass

    @abstractmethod
    def visit_mul_expression(self, element):
        pass

    @abstractmethod
    def visit_div_expression(self, element):
        pass

    @abstractmethod
    def visit_equality_operation(self, element):
        pass

    @abstractmethod
    def visit_relational_operation(self, element):
        pass

    @abstractmethod
    def visit_not_equal_operation(self, element):
        pass

    @abstractmethod
    def visit_greater_operation(self, element):
        pass

    @abstractmethod
    def visit_greater_equal_operation(self, element):
        pass

    @abstractmethod
    def visit_less_operation(self, element):
        pass

    @abstractmethod
    def visit_less_equal_operation(self, element):
        pass

    @abstractmethod
    def visit_bool_value(self, element):
        pass

    @abstractmethod
    def visit_integer_value(self, element):
        pass

    @abstractmethod
    def visit_float_value(self, element):
        pass

    @abstractmethod
    def visit_string_value(self, element):
        pass

    @abstractmethod
    def visit_null_value(self, element):
        pass

    @abstractmethod
    def visit_dictionary(self, element):
        pass

    @abstractmethod
    def visit_dictionary_entry(self, element):
        pass

    @abstractmethod
    def visit_assignment(self, element):
        pass

    @abstractmethod
    def visit_type_match(self, element):
        pass

    @abstractmethod
    def visit_match_case(self, element):
        pass

    @abstractmethod
    def visit_function_call(self, element):
        pass

    @abstractmethod
    def visit_object_access(self, element):
        pass

    @abstractmethod
    def visit_block(self, element):
        pass

    @abstractmethod
    def visit_string_type(self, element):
        pass

    @abstractmethod
    def visit_integer_type(self, element):
        pass

    @abstractmethod
    def visit_bool_type(self, element):
        pass

    @abstractmethod
    def visit_float_type(self, element):
        pass

    @abstractmethod
    def visit_variant_type(self, element):
        pass

    @abstractmethod
    def visit_void_type(self, element):
        pass

    @abstractmethod
    def visit_any_type(self, element):
        pass

    @abstractmethod
    def visit_dictionary_type(self, element):
        pass

    @abstractmethod
    def visit_break_statement(self, element):
        pass

    @abstractmethod
    def visit_declaration(self, element):
        pass