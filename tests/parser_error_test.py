from src.errors.parser_errors import SameParameterError
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import AndExpression, Assignment, Block, BoolType, DivExpression, EqualityOperation, FloatType, ForEachStatement, FunctionArguments, FunctionCall, Identifier, IntegerType, IntegerValue, LessOperation, MatchCase, MulExpression, Negation, ObjectAccess, Parameter, FunctionDefintion, StringType, StringValue, SumExpression, TypeExpression, TypeMatch
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
    exp_type = IntegerType((1, 1), 'int') # zrobić coś takiego wszędzie
    assert type == exp_type


def test_parameters():
    source_code = "int a, float a"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    parameters = parser.parse_parameters()
    exp_int = IntegerType((1, 1), 'int')
    exp_float = FloatType((1, 8), 'float')
    expected_parameters = []
    expected_parameters.append(Parameter((1, 1), exp_int, 'a'))
    expected_parameters.append(Parameter((1, 8), exp_float, 'b'))
    assert parameters == expected_parameters

def test_parameters1():
    source_code = "int a, float a"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)
    with pytest.raises(SameParameterError) as excinfo:
        parser.parse_parameters()