# from src.lexer.lexer import Lexer
# # from src.lexer.source import String, File
# from src.lexer.tokens import TokenType, Token
# from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, NumberTooLongError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
# import pytest
# import io



# def test_nested_comments():
#     source = io.StringIO("# Comment1\n123 # Comment2\n456")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.COMMENT
#     assert token.value == "# Comment1"
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 123
#     token = lexer.get_next_token()
#     assert token.type == TokenType.COMMENT
#     assert token.value == "# Comment2"
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 456


# def test_invalid_identifier_start():
#     source = io.StringIO("123abc")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 123
#     errors = lexer.error_manager.get_all_errors()
#     assert isinstance(errors[0], InvalidTokenError)
#     assert errors[0].message == "LexicalError (1, 4): Niezgodny znak: 'a'."


# def test_unterminated_string():
#     source = io.StringIO('"Hello world')
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     errors = lexer.error_manager.get_all_errors()
#     assert isinstance(errors[0], InvalidTokenError)
#     assert errors[0].message == "UnterminatedStringError (1, 1): String nie został poprawnie zakończony."


# def test_unexpected_characters_in_numbers():
#     source = io.StringIO("1,234 56.78.90")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     errors = lexer.error_manager.get_all_errors()
#     assert isinstance(errors[0], InvalidTokenError)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.FLOAT_VALUE 
#     token = lexer.get_next_token()
#     errors = lexer.error_manager.get_all_errors()
#     assert isinstance(errors[1], InvalidTokenError)


# def test_escape_sequences_in_strings():
#     source = io.StringIO('"Hello\\nWorld" "\\tIndented"')
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.STRING_VALUE
#     assert token.value == "Hello\nWorld"
#     token = lexer.get_next_token()
#     assert token.type == TokenType.STRING_VALUE
#     assert token.value == "\tIndented"


# def test_escape_sequences_in_strings2():
#     source = io.StringIO('"H\\j"')
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.STRING_VALUE
#     assert token.value == "Hj"
#     errors = lexer.error_manager.get_all_errors()
#     assert len(errors) == 1


# def test_mixed_whitespace_handling():
#     source = io.StringIO("   \t  \n  abc   \t\n  123   \n")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.value == "abc"
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 123
#     token = lexer.get_next_token()
#     assert token.type == TokenType.EOF


# def test_large_numbers():
#     source = io.StringIO("2147483647 2147483648 999999999999999999999")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.INTEGER_VALUE
#     assert token.value == 2147483647 
#     token = lexer.get_next_token()
#     errors = lexer.error_manager.get_all_errors()
#     assert isinstance(errors[0], InvalidTokenError)
#     token = lexer.get_next_token()
#     assert isinstance(errors[1], InvalidTokenError)


# def test_unicode_characters_in_identifiers():
#     source = io.StringIO("długopis cena_za_jabłko")
#     lexer = Lexer(source)
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.value == "długopis"
#     token = lexer.get_next_token()
#     assert token.type == TokenType.IDENTIFIER
#     assert token.value == "cena_za_jabłko"
