from src.lexer.lexer import Lexer
from src.lexer.source import String, File
from src.lexer.tokens import TokenType, Token
# from src.errors.lexer_errors import InvalidTokenError
import pytest
import io


def test_a1():
    l = Lexer(io.StringIO("text"))
    a=l._get_next_char()
    assert a == "e"



# def test_source1():
#     l = Lexer(io.StringIO("ab\r\na\rb"))
#     assert l._get_current_char() == "a"
#     assert l._get_current_position() == (1, 1)
#     assert l._get_next_char() == "b"
#     assert l._get_current_position() == (2, 1)
#     assert l._get_next_char() == "\n"
#     assert l._get_current_position() == (1, 2)
#     assert l.get_next_char() == "a"
#     assert l.get_current_position() == (1, 2)
#     assert l.get_next_char() == "\r"
#     assert l.get_current_position() == (2, 2)
#     assert l.get_next_char() == "b"
#     assert l.get_current_position() == (3, 2)


def test_source_positions1():
    l = Lexer(io.StringIO("ab\r\na\rb"))
    assert l._get_current_char() == "a"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (2, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (3, 1)
    assert l._get_next_char() == "a"
    assert l._get_current_position() == (1, 2)
    assert l._get_next_char() == "\r"
    assert l._get_current_position() == (2, 2)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (1, 3)


def test_source_positions2():
    l = Lexer(io.StringIO("\nb\r\na\rb"))
    assert l._get_current_char() == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (1, 2)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (2, 2)
    assert l._get_next_char() == "a"
    assert l._get_current_position() == (1, 3)
    assert l._get_next_char() == "\r"
    assert l._get_current_position() == (2, 3)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (1, 4)

def test_source_positions3():
    l = Lexer(io.StringIO("\n\n\r\na\rb"))
    assert l._get_current_char() == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (1, 2)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (1, 3)
    assert l._get_next_char() == "a"
    assert l._get_current_position() == (1, 4)
    assert l._get_next_char() == "\r"
    assert l._get_current_position() == (2, 4)
    assert l._get_next_char() == "b"
    assert l._get_current_position() == (1, 5)

def test_source_positions4():
    l = Lexer(io.StringIO("\r\n\r\n"))
    assert l._get_current_char() == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (1, 2)

def test_source_positions5():
    l = Lexer(io.StringIO("\r\n\r\r\n"))
    assert l._get_current_char() == "\n"
    assert l._get_current_position() == (1, 1)
    assert l._get_next_char() == "\r"
    assert l._get_current_position() == (1, 2)
    assert l._get_next_char() == "\n"
    assert l._get_current_position() == (1, 3)


# def test_source1():
#     l = Lexer(io.StringIO("\r\na\rb"))
#     assert l._get_current_char() == "\n"
#     assert l._get_current_position() == (1, 1)
    # assert l.get_next_char() == "a"
    # assert l.get_current_position() == (1, 2)
    # assert l.get_next_char() == "\r"
    # assert l.get_current_position() == (2, 2)
    # assert l.get_next_char() == "b"
    # assert l.get_current_position() == (3, 2)



# def test_source_get_position():
#     source = String("a")
#     assert source.get_current_position() == (1, 1)


# def test_source_get_current_char():
#     source = String("a")
#     assert source.get_current_char() == 'a'

# def test_source_set_start_position():
#     source = String("ab")
#     source.get_next_char()
#     assert source.get_current_position() == (2, 1)
#     assert source.get_current_char() == 'b'
#     source.set_start_position()
#     assert source.get_current_char() == 'a'
#     assert source.get_current_position() == (1, 1)


# def test_source_get_line():
#     source = String("a\nb")
#     assert source.get_line(1) == "a\n"
#     assert source.get_line(2) == "b"
#     assert source.get_line(3) == ""

# def test_source1():
#     source = String("\r\na\rb")
#     assert source.get_current_char() == "\n"
#     assert source.get_current_position() == (1, 1)
#     assert source.get_next_char() == "a"
#     assert source.get_current_position() == (1, 2)
#     assert source.get_next_char() == "\r"
#     assert source.get_current_position() == (2, 2)
#     assert source.get_next_char() == "b"
#     assert source.get_current_position() == (3, 2)

# def test_source_eof():
#     source = String("")
#     assert source.get_current_char() == ""
#     assert source.get_current_position() == (1, 1)
#     assert source.get_next_char() == ""
#     assert source.get_current_position() == (1, 1)


# def test_not_terminated_string():
#     source = String("\"abc")
    

# def test_lexer_skip_spaces():
#     lexer = Lexer(String("              a"))
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.value == "a"
#     assert token.position == (15, 1)

# def test_identifier_or_keyword():
#     source = String("if condition")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IF
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER

# def test_number():
#     source = String("123 45.67 ")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     token = lexer.get_next_token()
#     assert token.type == TokenType.FLOAT_VALUE

# def test_string():
#     source = String('"hello" "world"')
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.STRING_VALUE
#     assert token.value == "hello"
#     token = lexer.get_next_token()
#     assert token.value == "world"

# def test_symbol():
#     source = String("+ -")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.PLUS
#     token = lexer.get_next_token()
#     assert token.type == TokenType.MINUS

# def test_double_symbol():
#     source = String("||")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.LOGICAL_OR

# def test_double_symbol2():
#     source = String("==")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EQUALS

# def test_comment():
#     source = String("# This is a comment\n123")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.COMMENT
#     assert token.value == "# This is a comment"
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE

# def test_eof():
#     source = String("")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF

# def test_unknown():
#     source = String("@")
#     lexer = Lexer(source)
#     with pytest.raises(InvalidTokenError):
#         lexer.get_next_token()


# def test_lexer():
#     source = String("if 123 \"hello\" + -")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IF
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     token = lexer.get_next_token()
#     assert token.type == TokenType.STRING_VALUE
#     token = lexer.get_next_token()
#     assert token.type == TokenType.PLUS
#     token = lexer.get_next_token()
#     assert token.type == TokenType.MINUS
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF


# def test_numbers():
#     source = String("123 45.67 890")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == "123"
#     assert token.position == (1, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.FLOAT_VALUE
#     assert token.value == "45.67"
#     assert token.position == (5, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == "890"
#     assert token.position == (11, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF
#     assert token.position == (14, 1)

# def test_identifiers_and_keywords():
#     source = String("if condition123 else variable")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IF
#     assert token.position == (1, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.position == (4, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.ELSE
#     assert token.position == (17, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.position == (22, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF
#     assert token.position == (30, 1)

# def test_many_new_lines():
#     source = String("v \na\n else\n\n\n d")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.position == (1, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.position == (1, 2)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.ELSE
#     assert token.position == (2, 3)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.position == (2, 6)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF
#     assert token.position == (3, 6)

# def test_read_file():
#     lexer = Lexer(File("tests/code_files/identifier.txt"))
#     lexer.get_next_token()

# def test_file_identifier():
#     lexer = Lexer(File("tests/code_files/identifier.txt"))
#     token_types = [token.type for token in lexer.get_all_tokens()]
#     assert token_types == [
#         TokenType.IDENTIFIER,
#     ]
# def test_numbers():
#     # Test podstawowych typów liczbowych
#     source = String("123 45.67 890")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 123  # wartość jako liczba całkowita, nie string
#     assert token.position == (1, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.FLOAT_VALUE
#     assert token.value == 45.67  # wartość jako liczba zmiennoprzecinkowa, nie string
#     assert token.position == (5, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 890
#     assert token.position == (11, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF
#     assert token.position == (14, 1)

# def test_leading_zeros():
#     # Test liczby z wiodącymi zerami
#     source = String("007 0.123 000123")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 7
#     assert token.position == (1, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.FLOAT_VALUE
#     assert token.value == 0.123
#     assert token.position == (5, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 123
#     assert token.position == (11, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF
#     assert token.position == (17, 1)

# def test_invalid_number_format():
#     # Test nieprawidłowego formatu liczby
#     source = String("12.34.56 999")
#     lexer = Lexer(source)
#     try:
#         token = lexer.get_next_token()
#         assert False, "Should have raised an exception for invalid number format"
#     except ValueError as e:
#         assert str(e) == "Invalid number format"
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 999
#     assert token.position == (10, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF
#     assert token.position == (13, 1)

# def test_multiple_tokens():
#     # Test mieszania liczb i innych tokenów
#     source = String("123 abc 456.78 def")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 123
#     assert token.position == (1, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.value == "abc"
#     assert token.position == (5, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.FLOAT_VALUE
#     assert token.value == 456.78
#     assert token.position == (9, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.value == "def"
#     assert token.position == (16, 1)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF
#     assert token.position == (19, 1)

# def test_lexer_file_source_all_tokens():
#     lexer = Lexer(File("tests/code_files/all_tokens.txt"))
#     token_types = [token.type for token in lexer.get_all_tokens()]
#     assert token_types == [
#         TokenType.INT,
#         TokenType.FLOAT,
#         TokenType.BOOL,
#         TokenType.STRING,
#         TokenType.CLASS,
#         TokenType.AS,
#         TokenType.MATCH,
#         TokenType.WHILE,
#         TokenType.IF,
#         TokenType.ELSE,
#         TokenType.TRUE,
#         TokenType.FALSE,
#         TokenType.VOID,
#         TokenType.RETURN,
#         TokenType.IS,
#         TokenType.PLUS,
#         TokenType.MINUS,
#         TokenType.MULTIPLY,
#         TokenType.DIVIDE,
#         TokenType.ASSIGN,
#         TokenType.GREATER_THAN,
#         TokenType.LESS_THAN,
#         TokenType.LPAREN,
#         TokenType.RPAREN,
#         TokenType.LBRACE,
#         TokenType.RBRACE,
#         TokenType.DOT,
#         TokenType.COMMA,
#         TokenType.SEMICOLON,
#         TokenType.NOT,
#         TokenType.COMMENT,
#         TokenType.EQUALS,
#         TokenType.NOT_EQUALS,
#         TokenType.LESS_THAN_EQUAL,
#         TokenType.GREATER_THAN_EQUAL,
#         TokenType.LOGICAL_OR,
#         TokenType.LOGICAL_AND,
#         TokenType.RETURN_SIGN,
#         TokenType.IDENTIFIER,
#         TokenType.INTEGER_VALUE,
#         TokenType.FLOAT_VALUE,
#         TokenType.STRING_VALUE,
#     ]