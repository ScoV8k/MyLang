from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import AndExpression, AnyType, Assignment, Block, BoolType, DivExpression, EqualityOperation, FloatType, ForEachStatement, FunctionArguments, FunctionCall, Identifier, IntegerType, IntegerValue, LessOperation, MatchCase, MulExpression, Negation, ObjectAccess, Parameter, FunctionDefintion, Program, StringType, StringValue, SumExpression, TypeExpression, TypeMatch, VoidType
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

    type = parser._parse_type()
    exp_type = IntegerType((1, 1), 'int')
    assert type == exp_type

def test_type_void():
    source_code = "void"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    type = parser._parse_type()
    assert type == None

def test_type_void2():
    source_code = "void"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    type = parser._parse_func_type()
    exp_type = VoidType((1, 1), 'void')
    assert type == exp_type


def test_parameter2():
    source_code = "int elo"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    param = parser._parse_parameter()
    exp_type = IntegerType((1, 1), 'int')
    expected_param = Parameter((1, 1), exp_type, 'elo')
    assert param == expected_param

def test_parameter3():
    source_code = "int elo;"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    param = parser._parse_declaration()
    exp_type = IntegerType((1, 1), 'int')
    expected_param = Parameter((1, 1), exp_type, 'elo')
    assert param == expected_param


def test_parameters():
    source_code = "int a, float b, bool c, string d"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    parameters = parser._parse_parameters()
    exp_int = IntegerType((1, 1), 'int')
    exp_float = FloatType((1, 8), 'float')
    exp_bool = BoolType((1, 17), 'bool')
    exp_string = StringType((1, 25), 'string')
    expected_parameters = []
    expected_parameters.append(Parameter((1, 1), exp_int, 'a'))
    expected_parameters.append(Parameter((1, 8), exp_float, 'b'))
    expected_parameters.append(Parameter((1, 17), exp_bool, 'c'))
    expected_parameters.append(Parameter((1, 25), exp_string, 'd'))
    assert parameters == expected_parameters



def test_identifier_or_function_call():
    source_code = "elo get()"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    identifier = parser._parse_identifier_or_function_call()
    funcall = parser._parse_identifier_or_function_call()
    expected_identifier = Identifier((1,1), 'elo')
    expected_funcall = FunctionCall((1,5), 'get', None)
    assert identifier == expected_identifier
    # assert funcall == expected_funcall

def test_object_access():
    source_code = "elo.get()"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    obj_access = parser._parse_object_access()
    expected_identifier = Identifier((1,1), 'elo')
    expected_funcall = FunctionCall((1,5), 'get', [])
    expected_object_access = ObjectAccess((1, 1), [expected_identifier, expected_funcall])
    assert obj_access == expected_object_access


def test_literal():
    source_code = "123"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    literal = parser._parse_literal()
    expected_literal = IntegerValue((1, 1), 123)
    assert literal == expected_literal

def test_string_factor():
    source_code = "\"abc\""
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    literal = parser._parse_factor()
    expected_literal = StringValue((1, 1), "abc")
    assert literal == expected_literal

def test_type_expression():
    source_code = "\"abc\" is float"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    literal = parser._parse_type_expression()
    expected_factor = StringValue((1, 1), "abc")
    float_type = FloatType((1, 10), 'float')
    expected_literal = TypeExpression((1, 1), expected_factor, float_type)
    assert literal == expected_literal


def test_unary_expression():
    source_code = "not \"abc\" is float"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser._parse_unary_expression()
    expected_factor = StringValue((1, 5), "abc")
    float_type = FloatType((1, 14), 'float')
    expected_type_expression = TypeExpression((1, 5), expected_factor, float_type)
    expected_unary_expression = Negation((1, 1), expected_type_expression)
    assert expression == expected_unary_expression


def test_mul_expression():
    source_code = "-5 * 3 / 2"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser._parse_multiplication_expression()
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

    expression = parser._parse_add_expression()
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

    expression = parser._parse_relational_expression()
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

    expression = parser._parse_equality_expression()
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

    expression = parser._parse_and_expression()
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
    source_code = "match a {null => {abc();} _ => {a();}}"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser._parse_type_match()
    a = Identifier((1, 7), 'a')
    fun_call = FunctionCall((1, 19), 'abc', [])
    fun_call2 = FunctionCall((1, 33), 'a', [])
    block1 = Block((1, 18), [fun_call])
    block2 = Block((1, 32), [fun_call2])
    match_case1 = MatchCase((1, 10), VoidType((1, 10), "null"), block1)
    match_case2 = MatchCase((1, 27), AnyType((1, 27), "_"), block2)
    cases = [match_case1, match_case2]
    expected = TypeMatch((1, 1), a, cases, None)
    assert expression == expected



def test_block():
    source_code = "{abc();}"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    expression = parser._parse_block()
    fun_call = FunctionCall((1, 2), 'abc', [])
    block = Block((1, 1), [fun_call])
    assert expression == block



def test__parse_for_each_loop():
    source_code = "for each (key, value) in myDict { doSomething(); }"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    for_each_loop = parser._parse_for_each_loop()
    
    expected_key = "key"
    expected_value = "value"
    expected_expr = Identifier((1, 26), "myDict")
    expected_block = Block((1, 33), [
        FunctionCall((1, 35), "doSomething", [])
    ])
    expected = ForEachStatement((1, 1), expected_key, expected_value, expected_expr, expected_block)
    
    assert for_each_loop == expected


def test__parse_program_with_for_each_loop():
    source_code = "int main() {for each (key, value) in myDict { doSomething(); }}"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    program = parser.parse_program()
    print(program)
    expected_key = "key"
    expected_value = "value"
    expected_expr = Identifier((1, 38), "myDict")
    expected_block1 = Block((1, 45), [
        FunctionCall((1, 47), "doSomething", [])
    ])
    integer_type = IntegerType((1, 1), 'int')
    expected_for_each = ForEachStatement((1, 13), expected_key, expected_value, expected_expr, expected_block1)
    expected_block2 = Block((1, 12), [expected_for_each])
    expected_function_def = FunctionDefintion((1, 1), integer_type, 'main', [], expected_block2)
    expected_program = Program((1, 1), [expected_function_def])
    assert program == expected_program


