from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import FunctionArguments, Parameter, FunctionDefintion
# from src.lexer.source import String, File
from src.lexer.tokens import TokenType, Token
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, LeadingZeroError,NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
import pytest
import io



def test_simple_expression():
    source_code = "3 + 5"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer)

    # Oczekiwane drzewo składniowe (AST)
    expected_ast = {
        "type": "BinaryOperation",
        "operator": "+",
        "left": {"type": "Number", "value": 3},
        "right": {"type": "Number", "value": 5},
    }

    # Parsowanie kodu
    ast = parser.parse()
    assert ast == expected_ast, f"AST mismatch: {ast}"

def test_parser1():
    source_code = "int elo(int abc) { }"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    result = parser.parse_program()
    assert str(result) == "Function"

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
    expected = FunctionDefintion((1, 1), "funkcja", [expected_param], [])
    assert a == expected
