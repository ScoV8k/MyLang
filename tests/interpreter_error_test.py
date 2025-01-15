import io
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.errors.error_manager import ErrorManager
from src.interpreter.interpreter import Interpreter
from src.interpreter.execute_visitor import ExecuteVisitor
from src.errors.parser_errors import InvalidTypeExpression
from src.errors.interpreter_errors import DeclarationError, MainFunctionRequired, AssignmentError

def execute_code(source_code):
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


def test_recursion_limit():
    source_code = """
    int foo(int x) {
        return foo(x + 1);
    }

    int main() {
        return foo(0);
    }
    """
    with pytest.raises(RecursionError):
        execute_code(source_code)


def test_no_main_function():
    source_code = """
    int foo() {
        return 1;
    }
    """
    with pytest.raises(MainFunctionRequired):
        execute_code(source_code)


def test_break_outside_while():
    source_code = """
    int main() {
        break;
        return 0;
    }
    """
    with pytest.raises(RuntimeError):
        execute_code(source_code)


def test_assignment_error_not_declared():
    source_code = """
    int main() {
        x = 5;
        return 0;
    }
    """
    with pytest.raises(AssignmentError):
        execute_code(source_code)
