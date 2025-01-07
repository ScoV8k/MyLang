import io
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.errors.error_manager import ErrorManager
from src.interpreter.interpreter import Interpreter
from src.interpreter.ex_vis import ExecuteVisitor
from src.parser.objects import IntegerValue


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


def test_variable_assignment():
    source_code = """
    int main() {
        int a = 10;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == 10


def test_arithmetic_operations():
    source_code = """
    int main() {
        int a = 5 + 3 * 2;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == 11


def test_function_call():
    source_code = """
    int add(int a, int b) {
        return a + b;
    }

    int main() {
        int result = add(10, 20);
        return result;
    }
    """
    result = execute_code(source_code)
    assert result == 30


def test_conditional_statement():
    source_code = """
    int main() {
        int a = 10;
        if (a > 5) {
            return 1;
        } else {
            return 0;
        }
    }
    """
    result = execute_code(source_code)
    assert result == 1


def test_type_expression_true():
    source_code = """
    int main() {
        int a = 0;
        bool b = a is int;
        return b;
    }
    """
    result = execute_code(source_code)
    assert result == True



def test_type_expression_false():
    source_code = """
    int main() {
        int a = 0;
        bool b = a is float;
        return b;
    }
    """
    result = execute_code(source_code)
    assert result == False


def test_negation_logic_int():
    source_code = """
    int main() {
        int a = not 5;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == False

def test_negation_logic_not_keyword():
    source_code = """
    int main() {
        int a = not 1;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == 0  # Logical NOT of truthy value should return 0 (False)

def test_negation_logic_exclamation():
    source_code = """
    int main() {
        int a = !0;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == 1  # Logical NOT of falsy value should return 1 (True)

def test_negation_arithmetic():
    source_code = """
    int main() {
        int a = -5;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == -5  # Arithmetic negation should preserve sign

def test_mixed_negations():
    source_code = """
    int main() {
        int a = not (-5);
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == 0  # Logical negation of non-zero value should return 0

def test_negation_edge_case_zero():
    source_code = """
    int main() {
        int a = not 0;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == 1  # Logical NOT of zero should return 1 (True)


def test_type_match_int():
    source_code = """
    int main() {
        int x = 42;
        match x {
            int => {
                return 111;
            }
            _ => {
                return 999;
            }
        }
    }
    """
    result = execute_code(source_code)
    assert result == 111