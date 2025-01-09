import io
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.errors.error_manager import ErrorManager
from src.interpreter.interpreter import Interpreter
from src.interpreter.ex_vis import ExecuteVisitor
from src.errors.parser_errors import InvalidTypeExpression


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
