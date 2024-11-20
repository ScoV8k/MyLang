from src.lexer.lexer import Lexer
# from src.lexer.source import String, File
from src.lexer.tokens import TokenType, Token
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, LeadingZeroError,NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
import pytest
import io

MAX_IDENTIFIER_LENGTH = 128
MAX_INT = 2147483647
MAX_FLOAT = 3.402823466e+38
MAX_STRING_LENGTH = 2**16
MAX_COMMENT_LENGTH = 256
MAX_WHITESPACES = 1024


def run_lexer_test(source_code, expected_tokens, expected_errors):
    error_manager = ErrorManager()
    lexer = Lexer(io.StringIO(source_code), error_manager)
    actual_tokens = []
    while True:
        token = lexer.get_next_token()
        actual_tokens.append(token)
        if token.type == TokenType.EOF:
            break

    actual_errors = lexer.error_manager.get_all_errors()
    assert actual_tokens == expected_tokens
    assert actual_errors == expected_errors

def test_lexer_positions():
    l = Lexer(io.StringIO("ab\r\na\rb"), ErrorManager())
    assert l.current_char == "a"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (1, 2)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (1, 3)
    assert l._get_next_char() == "a"
    assert l._get_current_position() == (2, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (2, 2)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (3, 1)


def test_lexer_eof_position_not_incrementing():
    l = Lexer(io.StringIO("a"), ErrorManager())
    assert l.current_char == "a"
    l._get_next_char()
    assert l.current_char == ""
    assert l._get_current_position() == (1,2)
    l._get_next_char()
    assert l.current_char == ""
    assert l._get_current_position() == (1,2)

def test_lexer_positions_start_with_newline():
    l = Lexer(io.StringIO("\nb\r\na\rb"), ErrorManager())
    assert l.current_char == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (2, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (2, 2)
    assert l._get_next_char() == "a"
    assert l._get_current_position() == (3, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (3, 2)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (4, 1)

def test_lexer_positions_start_with_several_newlines():
    l = Lexer(io.StringIO("\n\n\r\na\rb"), ErrorManager())
    assert l.current_char == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (2, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (3, 1)
    assert l._get_next_char() == "a"
    assert l._get_current_position() == (4, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (4, 2)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (5, 1)

def test_lexer_positions_different_newlines():
    l = Lexer(io.StringIO("\r\n\r\n"), ErrorManager())
    assert l.current_char == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (2, 1)

def test_lexer_positions_different_newlines2():
    l = Lexer(io.StringIO("\r\n\r\r\n"), ErrorManager())
    assert l.current_char == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (2, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (3, 1)


def test_lexer_skip_spaces():
    source_code = "   a"
    expected_tokens = [
        Token(TokenType.IDENTIFIER, "a", (1, 4)),
        Token(TokenType.EOF, None, (1, 5)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_identifier_or_keyword():
    source_code = "if condition"
    expected_tokens = [
        Token(TokenType.IF, "if", (1, 1)),
        Token(TokenType.IDENTIFIER, "condition", (1, 4)),
        Token(TokenType.EOF, None, (1, 13)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_integer_and_float():
    source_code = "123 45.67 "
    expected_tokens = [
        Token(TokenType.INTEGER_VALUE, 123, (1, 1)),
        Token(TokenType.FLOAT_VALUE, 45.67, (1, 5)),
        Token(TokenType.EOF, None, (1, 11)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_string():
    source_code = '"hello" "world"'
    expected_tokens = [
        Token(TokenType.STRING_VALUE, "hello", (1, 1)),
        Token(TokenType.STRING_VALUE, "world", (1, 9)),
        Token(TokenType.EOF, None, (1, 16)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_single_symbols():
    source_code = "= + - * / ( ) { } ; , . : < > ! #"
    expected_tokens = [
        Token(TokenType.ASSIGN, "=", (1, 1)),
        Token(TokenType.PLUS, "+", (1, 3)),
        Token(TokenType.MINUS, "-", (1, 5)),
        Token(TokenType.MULTIPLY, "*", (1, 7)),
        Token(TokenType.DIVIDE, "/", (1, 9)),
        Token(TokenType.LPAREN, "(", (1, 11)),
        Token(TokenType.RPAREN, ")", (1, 13)),
        Token(TokenType.LBRACE, "{", (1, 15)),
        Token(TokenType.RBRACE, "}", (1, 17)),
        Token(TokenType.SEMICOLON, ";", (1, 19)),
        Token(TokenType.COMMA, ",", (1, 21)),
        Token(TokenType.DOT, ".", (1, 23)),
        Token(TokenType.COLON, ":", (1, 25)),
        Token(TokenType.LESS_THAN, "<", (1, 27)),
        Token(TokenType.GREATER_THAN, ">", (1, 29)),
        Token(TokenType.NOT, "!", (1, 31)),
        Token(TokenType.COMMENT, "#", (1, 33)),
        Token(TokenType.EOF, None, (1, 34)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_double_symbols():
    source_code = "== != <= >= && || =>"
    expected_tokens = [
        Token(TokenType.EQUALS, "==", (1, 1)),
        Token(TokenType.NOT_EQUALS, "!=", (1, 4)),
        Token(TokenType.LESS_THAN_EQUAL, "<=", (1, 7)),
        Token(TokenType.GREATER_THAN_EQUAL, ">=", (1, 10)),
        Token(TokenType.LOGICAL_AND, "&&", (1, 13)),
        Token(TokenType.LOGICAL_OR, "||", (1, 16)),
        Token(TokenType.ARROW, "=>", (1, 19)),
        Token(TokenType.EOF, None, (1, 21)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_comment():
    source_code = "# This is a comment\n123"
    expected_tokens = [
        Token(TokenType.COMMENT, "# This is a comment", (1, 1)),
        Token(TokenType.INTEGER_VALUE, 123, (2, 1)),
        Token(TokenType.EOF, None, (2, 4)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_eof():
    source_code = ""
    expected_tokens = [
        Token(TokenType.EOF, None, (1, 1)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_unknown_char():
    source_code = "@"
    expected_tokens = [
        Token(TokenType.UNKNOWN, None, (1, 1)),
        Token(TokenType.EOF, None, (1, 2)),
    ]
    expected_errors = [
        UnknownTokenError((1, 1), "@"),
    ]

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_number2():
    source_code = "2)"
    expected_tokens = [
        Token(TokenType.INTEGER_VALUE, 2, (1, 1)),
        Token(TokenType.RPAREN, ")", (1, 2)),
        Token(TokenType.EOF, None, (1, 3)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_unknown_char2():
    source_code = "123$123"
    expected_tokens = [
        Token(TokenType.INTEGER_VALUE, 123, (1, 1)),
        Token(TokenType.UNKNOWN, None, (1, 4)),
        Token(TokenType.INTEGER_VALUE, 123, (1, 5)),
        Token(TokenType.EOF, None, (1, 8)),
    ]
    expected_errors = [
        UnknownTokenError((1, 4), "$"),
    ]

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_max_integer():
    source_code = "2147483647"
    expected_tokens = [
        Token(TokenType.INTEGER_VALUE, 2147483647, (1, 1)),
        Token(TokenType.EOF, None, (1, 11)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_overfloat_integer():
    source_code = "2147483648"
    expected_tokens = [
        Token(TokenType.INTEGER_VALUE, None, (1, 1)),
        Token(TokenType.EOF, None, (1, 11)),
    ]
    expected_errors = [
        NumberTooBigError((1, 1), 2147483648),
    ]

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_numbers_with_leading_zeros():
    source_code = "007 0.123 000123"
    expected_tokens = [
        Token(TokenType.INTEGER_VALUE, None, (1, 1)),
        Token(TokenType.FLOAT_VALUE, 0.123, (1, 5)),
        Token(TokenType.INTEGER_VALUE, None, (1, 11)),
        Token(TokenType.EOF, None, (1, 17)),
    ]
    expected_errors = [LeadingZeroError((1, 1)), LeadingZeroError((1, 11))]

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_invalid_float_number_format():
    source_code = "12.34.56"
    expected_tokens = [
        Token(TokenType.FLOAT_VALUE, 12.34, (1, 1)),
        Token(TokenType.DOT, ".", (1, 6)),
        Token(TokenType.INTEGER_VALUE, 56, (1, 7)),
        Token(TokenType.EOF, None, (1, 9)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_nested_comments():
    source_code = "# Comment1\n123 # Comment2\n456"
    expected_tokens = [
        Token(TokenType.COMMENT, "# Comment1", (1, 1)),
        Token(TokenType.INTEGER_VALUE, 123, (2, 1)),
        Token(TokenType.COMMENT, "# Comment2", (2, 5)),
        Token(TokenType.INTEGER_VALUE, 456, (3, 1)),
        Token(TokenType.EOF, None, (3, 4)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_invalid_identifier_start():
    source_code = "123abc"
    expected_tokens = [
        Token(TokenType.INTEGER_VALUE, 123, (1, 1)),
        Token(TokenType.IDENTIFIER, "abc", (1, 4)),
        Token(TokenType.EOF, None, (1, 7)),
    ]
    expected_errors = [
    ]

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_unterminated_string():
    source_code = '"Hello world'
    expected_tokens = [
        Token(TokenType.STRING_VALUE, "Hello world", (1, 1)),
        Token(TokenType.EOF, None, (1, 13)),
    ]
    expected_errors = [
        UnterminatedStringError((1, 1)),
    ]

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_unexpected_characters_in_numbers():
    source_code = "1,234 56.78.90"
    expected_tokens = [
        Token(TokenType.INTEGER_VALUE, 1, (1, 1)),
        Token(TokenType.COMMA, ",", (1, 2)),
        Token(TokenType.INTEGER_VALUE, 234, (1, 3)),
        Token(TokenType.FLOAT_VALUE, 56.78, (1, 7)),
        Token(TokenType.DOT, ".", (1, 12)),
        Token(TokenType.INTEGER_VALUE, 90, (1, 13)),
        Token(TokenType.EOF, None, (1, 15)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_escape_sequences_in_strings():
    source_code = '"Hello\\nWorld" "\\tIndented"'
    expected_tokens = [
        Token(TokenType.STRING_VALUE, "Hello\nWorld", (1, 1)),
        Token(TokenType.STRING_VALUE, "\tIndented", (1, 16)),
        Token(TokenType.EOF, None, (1, 28)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_escape_sequences_in_strings2():
    source_code = '"H\\j"'
    expected_tokens = [
        Token(TokenType.STRING_VALUE, "Hj", (1, 1)),
        Token(TokenType.EOF, None, (1, 6)),
    ]
    expected_errors = [
        InvalidEscapeSequenceError((1, 4), "j"),
    ]

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_mixed_whitespace_handling():
    source_code = "   \t  \n  abc   \t\n  123   \n"
    expected_tokens = [
        Token(TokenType.IDENTIFIER, "abc", (2, 3)),
        Token(TokenType.INTEGER_VALUE, 123, (3, 3)),
        Token(TokenType.EOF, None, (4, 1)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_large_numbers():
    source_code = "2147483647 2147483648 999999999999999999999"
    expected_tokens = [
        Token(TokenType.INTEGER_VALUE, 2147483647, (1, 1)),
        Token(TokenType.INTEGER_VALUE, None, (1, 12)),
        Token(TokenType.INTEGER_VALUE, None, (1, 23)),
        Token(TokenType.EOF, None, (1, 44)),
    ]
    expected_errors = [
        NumberTooBigError((1, 12), "2147483648"),
        NumberTooBigError((1, 23), "999999999999999999999"),
    ]

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_unicode_characters_in_identifiers():
    source_code = "długopis cena_za_jabłko"
    expected_tokens = [
        Token(TokenType.IDENTIFIER, "długopis", (1, 1)),
        Token(TokenType.IDENTIFIER, "cena_za_jabłko", (1, 10)),
        Token(TokenType.EOF, None, (1, 24)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_max_identifier_length():
    source_code = "a" * MAX_IDENTIFIER_LENGTH
    expected_tokens = [
        Token(TokenType.IDENTIFIER, source_code, (1, 1)),
        Token(TokenType.EOF, None, (1, MAX_IDENTIFIER_LENGTH + 1)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_too_long_identifier():
    source_code = "a" * (MAX_IDENTIFIER_LENGTH + 1)
    expected_tokens = [
        Token(TokenType.IDENTIFIER, source_code, (1, 1)),
        Token(TokenType.EOF, None, (1, MAX_IDENTIFIER_LENGTH + 2)),
    ]
    expected_errors = [
        IdentifierTooLongError((1, 1), source_code),
    ]

    run_lexer_test(source_code, expected_tokens, expected_errors)

def test_max_whitespaces():
    source_code = " " * MAX_WHITESPACES + "a"
    expected_tokens = [
        Token(TokenType.IDENTIFIER, "a", (1, MAX_WHITESPACES + 1)),
        Token(TokenType.EOF, None, (1, MAX_WHITESPACES + 2)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_too_many_whitespaces():
    source_code = " " * (MAX_WHITESPACES + 1) + "a"
    expected_tokens = [
        Token(TokenType.IDENTIFIER, "a", (1, MAX_WHITESPACES + 1)),
        Token(TokenType.EOF, None, (1, MAX_WHITESPACES + 2)),
    ]
    expected_errors = [TooManyWhitespacesError((1, 1))]

    run_lexer_test(source_code, expected_tokens, expected_errors)

def test_max_comment_length():
    source_code = "#" + "a" * (MAX_COMMENT_LENGTH - 1)
    expected_tokens = [
        Token(TokenType.COMMENT, source_code, (1, 1)),
        Token(TokenType.EOF, None, (1, MAX_COMMENT_LENGTH + 1)),
    ]
    expected_errors = []

    run_lexer_test(source_code, expected_tokens, expected_errors)


def test_too_long_comment():
    source_code = "#" + "a" * MAX_COMMENT_LENGTH
    expected_tokens = [
        Token(TokenType.COMMENT, source_code, (1, 1)),
        Token(TokenType.EOF, None, (1, MAX_COMMENT_LENGTH + 2)),
    ]
    expected_errors = [CommentTooLongError((1, 1))]

    run_lexer_test(source_code, expected_tokens, expected_errors)
