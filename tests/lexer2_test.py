from src.lexer.lexer import Lexer
from src.lexer.source import String, File
from src.lexer.tokens import TokenType, Token
from src.errors.lexer_errors import InvalidTokenError
import pytest
import io



def test_nested_comments():
    source = io.StringIO("# Comment1\n123 # Comment2\n456")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.COMMENT
    assert token.value == "# Comment1"
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_VALUE
    assert token.value == 123
    token = lexer.get_next_token()
    assert token.type == TokenType.COMMENT
    assert token.value == "# Comment2"
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_VALUE
    assert token.value == 456


def test_invalid_identifier_start():
    source = io.StringIO("123abc")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_VALUE
    assert token.value == 123
    errors = lexer.error_manager.get_all_errors()
    assert isinstance(errors[0], InvalidTokenError)
    assert errors[0].message == "LexicalError (1, 4): Niezgodny znak: 'a'."


def test_unterminated_string():
    # Testuje przypadek, gdy łańcuch tekstowy jest niedomknięty
    source = io.StringIO('"Hello world')
    lexer = Lexer(source)
    token = lexer.get_next_token()
    errors = lexer.error_manager.get_all_errors()
    assert isinstance(errors[0], InvalidTokenError)
    assert errors[0].message == "LexerError (1, 1): Niedomknięty łańcuch znaków."


def test_unexpected_characters_in_numbers():
    # Sprawdza nietypowe i błędne znaki w liczbach, np. separator tysięcy
    source = io.StringIO("1,234 56.78.90")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    errors = lexer.error_manager.get_all_errors()
    assert isinstance(errors[0], InvalidTokenError)  # ',' w liczbach jest niepoprawny
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT_VALUE  # Pierwszy poprawny float
    token = lexer.get_next_token()
    errors = lexer.error_manager.get_all_errors()
    assert isinstance(errors[1], InvalidTokenError)  # Drugi '.' w liczbie float jest niepoprawny


def test_escape_sequences_in_strings():
    # Testuje sekwencje escape w łańcuchach, np. \n, \t, itp.
    source = io.StringIO('"Hello\\nWorld" "\\tIndented"')
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.STRING_VALUE
    assert token.value == "Hello\nWorld"
    token = lexer.get_next_token()
    assert token.type == TokenType.STRING_VALUE
    assert token.value == "\tIndented"


def test_mixed_whitespace_handling():
    # Testuje skomplikowane sekwencje białych znaków (np. spacje, tabulatory, nowe linie)
    source = io.StringIO("   \t  \n  abc   \t\n  123   \n")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "abc"
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_VALUE
    assert token.value == 123
    token = lexer.get_next_token()
    assert token.type == TokenType.EOF


def test_large_numbers():
    # Testuje obsługę dużych liczb
    source = io.StringIO("2147483647 2147483648 999999999999999999999")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_VALUE
    assert token.value == 2147483647  # Maksymalna wartość 32-bitowego integera
    token = lexer.get_next_token()
    errors = lexer.error_manager.get_all_errors()
    assert isinstance(errors[0], InvalidTokenError)  # 2147483648 wykracza poza zakres
    token = lexer.get_next_token()
    assert isinstance(errors[1], InvalidTokenError)  # Błąd dla liczby poza zakresem


def test_unicode_characters_in_identifiers():
    # Testuje sytuację, gdy identyfikatory zawierają znaki Unicode (polskie znaki, itp.)
    source = io.StringIO("długopis cena_za_jabłko")
    lexer = Lexer(source)
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "długopis"
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "cena_za_jabłko"


def test_invalid_symbols_sequence():
    # Sprawdza niepoprawną sekwencję symboli, np. mieszanie operatorów bez operandów
    source = io.StringIO("+-*/")
    lexer = Lexer(source)
    for _ in range(4):
        token = lexer.get_next_token()
        assert token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE]
    errors = lexer.error_manager.get_all_errors()
    assert len(errors) == 3  # Trzy błędy, bo sąsiednie operatory bez operandów

    
def test_empty_or_whitespace_input():
    # Testuje pusty lub biały input, który powinien natychmiast zwrócić EOF
    sources = [io.StringIO(""), io.StringIO("   "), io.StringIO("\n\t")]
    for source in sources:
        lexer = Lexer(source)
        token = lexer.get_next_token()
        assert token.type == TokenType.EOF
