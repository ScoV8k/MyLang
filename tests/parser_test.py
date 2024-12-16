from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import AndExpression, Assignment, Block, DivExpression, EqualityOperation, FunctionArguments, FunctionCall, Identifier, IntegerValue, LessOperation, MatchCase, MulExpression, Negation, ObjectAccess, Parameter, FunctionDefintion, StringValue, SumExpression, TypeExpression, TypeMatch
# from src.lexer.source import String, File
from src.lexer.tokens import TokenType, Token
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, LeadingZeroError,NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
import pytest
import io


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
    int2 = IntegerValue((1, 6), 3)
    int3 = IntegerValue((1, 10), 2)
    int = IntegerValue((1, 2), 5)
    negation = Negation((1, 1), int)
    mul = MulExpression((1, 1), negation, int2)
    expected = DivExpression((1, 1), mul, int3)
    assert expression == expected


def test_add_expression():
    source_code = "-5 + 3 / 2"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser.parse_add_expression()
    int2 = IntegerValue((1, 6), 3)
    int3 = IntegerValue((1, 10), 2)
    int = IntegerValue((1, 2), 5)
    negation = Negation((1, 1), int)
    mul = MulExpression((1, 1), negation, int2)
    div = DivExpression((1, 6), int2, int3)
    expected = SumExpression((1, 1), negation, div)
    assert expression == expected


def test_relational_expression():
    source_code = "-5 + 3 < 2"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser.parse_relational_expression()
    int2 = IntegerValue((1, 6), 3)
    int3 = IntegerValue((1, 10), 2)
    int = IntegerValue((1, 2), 5)
    negation = Negation((1, 1), int)
    sum = SumExpression((1, 1), negation, int2)
    expected = LessOperation((1, 1), sum, int3)
    assert expression == expected


def test_equality_expression():
    source_code = "-5 + 3 == 2"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser.parse_equality_expression()
    int2 = IntegerValue((1, 6), 3)
    int3 = IntegerValue((1, 11), 2)
    int = IntegerValue((1, 2), 5)
    negation = Negation((1, 1), int)
    sum = SumExpression((1, 1), negation, int2)
    expected = EqualityOperation((1, 1), sum, int3)
    assert expression == expected

def test_and_expression():
    source_code = "a == 2 && b == 3"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser.parse_and_expression()
    a = Identifier((1, 1), 'a')
    int1 = IntegerValue((1, 6), 2)
    b = Identifier((1, 11), 'b')
    int2 = IntegerValue((1, 16), 3)
    eq1 = EqualityOperation((1, 1), a, int1)
    eq2 = EqualityOperation((1, 11), b, int2)
    expected_expressions = [eq1, eq2]
    expected = AndExpression((1, 1), expected_expressions)
    assert expression == expected


def test_type_match():
    source_code = "match a {null => {abc();}}"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser.parse_type_match()
    a = Identifier((1, 7), 'a')
    name = Identifier((1, 19), 'abc')
    fun_call = FunctionCall((1, 19), name, None)
    assignment = Assignment((1,19), fun_call, None)
    block = Block((1, 18), [assignment])
    match_case = MatchCase((1, 10), 'null', block)
    cases = [match_case]
    expected = TypeMatch((1, 1), a, cases, None)
    assert expression == expected



def test_type_match1():
    source_code = "{abc();}"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser.parse_block()
    a = Identifier((1, 7), 'a')
    name = Identifier((1, 2), 'abc')
    fun_call = FunctionCall((1, 2), name, None)
    assignment = Assignment((1, 2), fun_call, None)
    l = [assignment]
    block = Block((1, 1), l)
    match_case = MatchCase((1, 10), 'null', block)
    cases = [match_case]
    expected = TypeMatch((1, 1), a, cases, None)
    assert expression == block
