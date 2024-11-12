from src.lexer.lexer import Lexer
from src.lexer.source import String, File
from src.lexer.tokens import TokenType, Token
from src.errors.lexer_errors import InvalidTokenError
import pytest
import io


def test_lexer_positions():
    l = Lexer(io.StringIO("ab\r\na\rb"))
    assert l._get_current_char() == "a"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (1, 2)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (1, 3)
    assert l._get_next_char() == "a"
    assert l._get_current_position() == (2, 1)
    assert l._get_next_char() == "\r"
    assert l._get_current_position() == (2, 2)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (3, 1)


def test_lexer_positions_start_with_newline():
    l = Lexer(io.StringIO("\nb\r\na\rb"))
    assert l._get_current_char() == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (2, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (2, 2)
    assert l._get_next_char() == "a"
    assert l._get_current_position() == (3, 1)
    assert l._get_next_char() == "\r"
    assert l._get_current_position() == (3, 2)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (4, 1)

def test_lexer_positions_start_with_several_newlines():
    l = Lexer(io.StringIO("\n\n\r\na\rb"))
    assert l._get_current_char() == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (2, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (3, 1)
    assert l._get_next_char() == "a"
    assert l._get_current_position() == (4, 1)
    assert l._get_next_char() == "\r"
    assert l._get_current_position() == (4, 2)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (5, 1)

def test_lexer_positions_different_newlines():
    l = Lexer(io.StringIO("\r\n\r\n"))
    assert l._get_current_char() == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (2, 1)

def test_lexer_positions_different_newlines2():
    l = Lexer(io.StringIO("\r\n\r\r\n"))
    assert l._get_current_char() == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "\r"
    assert l._get_current_position() == (2, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (3, 1)


def test_lexer_skip_spaces():
    lexer = Lexer(io.StringIO("   a"))
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "a"
    assert token.position == (1, 4)

def test_identifier_or_keyword():
    source = io.StringIO("if condition")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.IF
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER

def test_integer_and_float():
    source = io.StringIO("123 45.67 ")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_VALUE
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT_VALUE

def test_string():
    source = io.StringIO('"hello" "world"')
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.STRING_VALUE
    assert token.value == "hello"
    token = lexer.get_next_token()
    assert token.value == "world"

def test_single_symbols():
    source = io.StringIO("= + - * / ( ) { } ; , . : < > ! #")
    lexer = Lexer(source)
    
    expected_tokens = [
        TokenType.ASSIGN, TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
        TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE,
        TokenType.SEMICOLON, TokenType.COMMA, TokenType.DOT, TokenType.COLON,
        TokenType.LESS_THAN, TokenType.GREATER_THAN, TokenType.NOT, TokenType.COMMENT
    ]
    
    for expected_token in expected_tokens:
        token = lexer.get_next_token()
        assert token.type == expected_token, f"Expected {expected_token}, got {token.type}"

def test_double_symbols():
    source = io.StringIO("== != <= >= && || =>")
    lexer = Lexer(source)
    
    expected_tokens = [
        TokenType.EQUALS, TokenType.NOT_EQUALS, TokenType.LESS_THAN_EQUAL,
        TokenType.GREATER_THAN_EQUAL, TokenType.LOGICAL_AND, TokenType.LOGICAL_OR,
        TokenType.ARROW
    ]
    
    for expected_token in expected_tokens:
        token = lexer.get_next_token()
        assert token.type == expected_token, f"Expected {expected_token}, got {token.type}"

def test_comment():
    source = io.StringIO("# This is a comment\n123")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.COMMENT
    assert token.value == "# This is a comment"
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_VALUE

def test_eof():
    source = io.StringIO("")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.EOF

def test_unknown_char():
    source = io.StringIO("@")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    errors = lexer.error_manager.get_all_errors()
    assert isinstance(errors[0], InvalidTokenError)
    # with pytest.raises(InvalidTokenError):
    #     lexer.get_next_token()

def test_unknown_char2():
    source = io.StringIO("123$123")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.value == 123
    errors = lexer.error_manager.get_all_errors()
    assert isinstance(errors[0], InvalidTokenError)
    # with pytest.raises(InvalidTokenError):
    #     lexer.get_next_token()

def test_numbers_with_leading_zeros():
    source = io.StringIO("007 0.123 000123")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_VALUE
    assert token.value == 7
    assert token.position == (1, 1)
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT_VALUE
    assert token.value == 0.123
    assert token.position == (1, 5)
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_VALUE
    assert token.value == 123
    assert token.position == (1, 11)
    token = lexer.get_next_token()
    assert token.type == TokenType.EOF
    assert token.position == (1, 17)

def test_invalid_float_number_format():
    source = io.StringIO("12.34.56")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    errors = lexer.error_manager.get_all_errors()
    assert isinstance(errors[0], InvalidTokenError)
    assert token.type == TokenType.FLOAT_VALUE

