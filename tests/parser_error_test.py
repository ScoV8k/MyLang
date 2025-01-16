from src.errors.parser_errors import BuildingFunctionError, EmptyBlockOfStatements, NoBlockInFunctionDefinition, NoExpressionInAssignment, NoExpressionInDeclaration, NoIdentifierAfterAs, NoIdentifierInDeclaration, NoTypeMatchExpressionError, SameParameterError, UnexpectedToken, UnexpectedTokenType
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import AndExpression, Assignment, Block, BoolType, DivExpression, EqualityOperation, FloatType, ForEachStatement, FunctionCall, Identifier, IntegerType, IntegerValue, LessOperation, MatchCase, MulExpression, Negation, ObjectAccess, Parameter, FunctionDefintion, StringType, StringValue, SumExpression, TypeExpression, TypeMatch
# from src.lexer.source import String, File
from src.lexer.tokens import TokenType, Token
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, LeadingZeroError,NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
import pytest
import io



def test_same_parameters():
    source_code = "int a, float a"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)
    with pytest.raises(SameParameterError):
        parser._parse_parameters()


def test_parse_function_definition_missing_identifier():
    source_code = "int 123()"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    with pytest.raises(BuildingFunctionError):
        parser.parse_program()

def test_parse_function_definition_missing_block():
    source_code = "int main()"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    with pytest.raises(NoBlockInFunctionDefinition):
        parser.parse_program()

def test_parse_block_missing_brace():
    source_code = "{ statement();"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    with pytest.raises(UnexpectedToken):
        parser.parse_program()

def test_parameter3():
    source_code = "int"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    with pytest.raises(NoIdentifierInDeclaration):
        parser._parse_parameter()

def test_parse_block_empty_block():
    source_code = "int main() { }"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    with pytest.raises(EmptyBlockOfStatements):
        parser.parse_program()


def test_parse_declaration_no_expression():
    source_code = "int main() {int x = ;}"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    with pytest.raises(NoExpressionInDeclaration):
        parser.parse_program()


def test_parse_assignment_no_expression():
    source_code = "int main() {x = ;}"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    with pytest.raises(NoExpressionInAssignment):
        parser.parse_program()


def test_parse_type_match_missing_identifier():
    source_code = "int main() {match x as { null => {} }}"
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)

    with pytest.raises(NoIdentifierAfterAs):
        parser.parse_program()
