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

def test_sum_expression():
    source_code = """
    int main() {
        int a = 5 + 3;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == 8

def test_sum_expression2():
    source_code = """
    int add(int a, int b) {
        return a + b + 10;
    }

    int main() {
        int result = add(10, 20) + 1;
        return result;
    }
    """
    result = execute_code(source_code)
    assert result == 41

def test_sum_different_types():
    source_code = """
    float main() {
        int a = 5 + 3;
        float b = 10.5 + 2;
        return b;
    }
    """
    result = execute_code(source_code)
    assert result == 12.5

def test_sub_expression():
    source_code = """
    int main() {
        int a = 5 - 3;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == 2

def test_sub_expression2():
    source_code = """
    int sub(int a, int b) {
        return a - b - 1;
    }

    int main() {
        int result = sub(20, 10) - 1;
        return result;
    }
    """
    result = execute_code(source_code)
    assert result == 8

def test_mul_expression2():
    source_code = """
    int mul(int a, int b) {
        return a * b * 1;
    }

    float main() {
        float result = mul(1, 3) * 0.5;
        return result;
    }
    """
    result = execute_code(source_code)
    assert result == 1.5

def test_mul_string():
    source_code = """
    string mul(int a, string b) {
        return a * b;
    }

    string main() {
        string result = mul(2, "abc");
        return result;
    }
    """
    result = execute_code(source_code)
    assert result == "abcabc"

def test_div_expression2():
    source_code = """
    int div(int a, int b) {
        return a / b / 1;
    }

    float main() {
        float result = div(10, 5) / 0.5;
        return result;
    }
    """
    result = execute_code(source_code)
    assert result == 4

def test_arithmetic_operations():
    source_code = """
    int main() {
        int a = 5 + 3 * 2;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == 11

def test_equality_operations():
    source_code = """
    bool main() {
        bool a = 2 == 2;
        return a;
    }
    """
    result = execute_code(source_code)
    assert result == True

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

# def test_type_match_float():
    source_code = """
    float main() {
        float y = 3.14;
        match y {
            int => {
                return 888;
            }
            float => {
                return 333;
            }
            _ => {
                return 999;
            }
        }
    }
    """
    result = execute_code(source_code)
    assert result == 333

def test_type_match_underscore():
    source_code = """
    int main() {
        bool b = true;
        match b {
            string => {return 1;}
            int => {
                return 111;
            }
            float => {
                return 222;
            }
            null => {return 2;}
            _ => {
                return 333;
            }
        }
    }
    """
    result = execute_code(source_code)
    assert result == 333


def test_type_match_variant_null():
    source_code = """
    int main() {
        variant something = null;

        match something {
            null => {
                return 123;
            }
            _ => {
                return 999;
            }
        }
    }
    """
    result = execute_code(source_code)
    assert result == 123


def test_type_match_variant_int_typematch_any():
    source_code = """
    int main() {
        variant something = 12;

        match something {
            null => {
                return 123;
            }
            _ => {
                return 999;
            }
        }
    }
    """
    result = execute_code(source_code)
    assert result == 999


def test_type_match_variant_int_typematch_int():
    source_code = """
    int main() {
        variant something = 12;

        match something {
            null => {
                return 123;
            }
            int => { return 12;}
            _ => {
                return 999;
            }
        }
    }
    """
    result = execute_code(source_code)
    assert result == 12


def test_type_match_as_identifier():
    source_code = """
    int main() {
        match (1 + 2) as foo {
            int => {
                return foo; 
            }
            _ => {
                return 999;
            }
        }
    }
    """
    result = execute_code(source_code)
    assert result == 3


def test_type_match_as_identifier2():
    source_code = """
    int type() {
        match (1 + 2) as three {
            null => {return 0;}
            int => {return three+1;}}}

    int main() {
        int result = type();
        return result;
    }
    """
    result = execute_code(source_code)
    assert result == 4
