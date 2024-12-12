from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import FunctionArguments, FunctionCall, Identifier, IntegerValue, MulExpression, Negation, ObjectAccess, Parameter, FunctionDefintion, StringValue, TypeExpression
# from src.lexer.source import String, File
from src.lexer.tokens import TokenType, Token
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, LeadingZeroError,NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
import pytest
import io



def test_parameter():
    source_code = "int a"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    a = parser.parse_parameter()
    ecp = Parameter((1, 5), "int", "a")
    assert a == ecp


def test_function():
    source_code = "void funkcja(float a) { }"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    a = parser.parse_function_definition()
    expected_param = Parameter((1, 20), "float", "a")
    expected = FunctionDefintion((1, 1), "funkcja", [expected_param], None)
    assert a == expected

def test_type():
    source_code = "int"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    type = parser.parse_type()
    expected_type = 'int'
    assert type == expected_type

def test_type_or_variant():
    source_code = "float variant"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    type = parser.parse_type_or_varinat()
    type2 = parser.parse_type_or_varinat()
    expected_type = 'float'
    expected_variant = 'variant'
    assert type == expected_type
    assert type2 == expected_variant


def test_identifier():
    source_code = "witam"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    type = parser.parse_identifier()
    expected_type = Identifier((1,1), 'witam')
    assert type == expected_type


def test_parameter2():
    source_code = "int elo"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    type = parser.parse_parameter()
    expected_type = Parameter((1, 1), 'int', 'elo')
    assert type == expected_type

def test_parameters():
    source_code = "int a, float b, bool c, string d"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    parameters = parser.parse_parameters()
    expected_parameters = []
    expected_parameters.append(Parameter((1, 1), 'int', 'a'))
    expected_parameters.append(Parameter((1, 8), 'float', 'b'))
    expected_parameters.append(Parameter((1, 17), 'bool', 'c'))
    expected_parameters.append(Parameter((1, 25), 'string', 'd'))
    assert parameters == expected_parameters



def test_identifier_or_function_call():
    source_code = "elo get()"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    identifier = parser.parse_identifier_or_function_call()
    funcall = parser.parse_identifier_or_function_call()
    expected_identifier = Identifier((1,1), 'elo')
    expected_identifier2 = Identifier((1,5), 'get')
    expected_funcall = FunctionCall((1,5), expected_identifier2, None)
    assert identifier == expected_identifier
    assert funcall == expected_funcall

def test_object_access():
    source_code = "elo.get()"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    obj_access = parser.parse_object_access()
    expected_identifier = Identifier((1,1), 'elo')
    expected_identifier2 = Identifier((1,5), 'get')
    expected_funcall = FunctionCall((1,5), expected_identifier2, None)
    expected_object_access = ObjectAccess((1, 1), expected_identifier, [expected_funcall])
    assert obj_access == expected_object_access


def test_literal():
    source_code = "123"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    literal = parser.parse_literal()
    expected_literal = IntegerValue((1, 1), 123)
    assert literal == expected_literal

def test_string_factor():
    source_code = "\"abc\""
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    literal = parser.parse_factor()
    expected_literal = StringValue((1, 1), "abc")
    assert literal == expected_literal

def test_type_expression():
    source_code = "\"abc\" is float"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    literal = parser.parse_type_expression()
    expected_factor = StringValue((1, 1), "abc")
    expected_literal = TypeExpression((1, 1), expected_factor, "float")
    assert literal == expected_literal


def test_unary_expression():
    source_code = "not \"abc\" is float"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser.parse_unary_expression()
    expected_factor = StringValue((1, 5), "abc")
    expected_type_expression = TypeExpression((1, 5), expected_factor, "float")
    expected_unary_expression = Negation((1, 1), expected_type_expression)
    assert expression == expected_unary_expression


def test_mul_expression():
    source_code = "-5 * 3 / 2"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser.parse_multiplication_expression()
    expected_factor = IntegerValue((1, 2), 5)
    expected_type_expression = TypeExpression((1, 1), expected_factor, "int")
    expected_unary_expression = Negation((1, 1), expected_type_expression)
    expected_mul_expression = MulExpression((1, 1), )
    assert expression == expected_unary_expression
