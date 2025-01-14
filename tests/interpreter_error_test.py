import io
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.errors.error_manager import ErrorManager
from src.interpreter.interpreter import Interpreter
from src.interpreter.execute_visitor import ExecuteVisitor
from src.errors.parser_errors import InvalidTypeExpression
from src.errors.interpreter_errors import DeclarationError


def execute_code(source_code):
    """Helper function to execute source code and return the result."""
    source = io.StringIO(source_code)
    error_manager = ErrorManager()
    lexer = Lexer(source, error_manager)
    parser = Parser(lexer, error_manager)
    program = parser.parse_program()

    visitor = ExecuteVisitor()
    interpreter = Interpreter(program)
    return interpreter.execute(visitor)


def test_type_expression_missing_type():
    source_code = """
    int main() {
        int a = 5;
        bool b = a is ;
        return b;
    }
    """
    with pytest.raises(InvalidTypeExpression):
        execute_code(source_code)


def test_redeclaration_error():
    source_code = """
    int main() {
        int a = 10;
        int a = 20;
        return a;
    }
    """
    with pytest.raises(DeclarationError):
        execute_code(source_code)
