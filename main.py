from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import AndExpression, Assignment, Block, BoolType, DivExpression, EqualityOperation, FloatType, ForEachStatement, FunctionArguments, FunctionCall, Identifier, IntegerType, IntegerValue, LessOperation, MatchCase, MulExpression, Negation, ObjectAccess, Parameter, FunctionDefintion, Program, StringType, StringValue, SumExpression, TypeExpression, TypeMatch
from src.lexer.tokens import TokenType, Token
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, LeadingZeroError,NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
# from src.interpreter.visitor import Visitor
from src.interpreter.print_visitor import PrintVisitor
from src.interpreter.interpreter import Interpreter
from src.interpreter.execute_visitor import ExecuteVisitor
import sys
import io




# source_code = "int main() {for each (key, value) in myDict { doSomething(); }}"
# source_code = "int main() {for each (key, value) in myDict { doSomething(); }} void abc() {int a = 123; dict g = {1: \"abc\", 2: 123};}"
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

a = """
    int main() {
    int a = 10;
    return a;}
"""

b = """
    int add(int a, int b) {
        return a + b + 10;
    }

    int main() {
        int result = add(10, 20) + 1;
        return result;
    }
    """
c = """
    int main() {
        int a = 5 + 2 * 8;
        return a;
    }
    """

d = """
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

abc = """
    int main() {
        int a = 0;
        while (a < 5) {
            a = a + 1;
        }
        return a;
    }
    """
test = """
    dict main() {
        dict a = {"key": 1};
        a.get("key");
    }
    """

abc = """
    int main() {
        dict a = {"key": 1};
        for each (key, value) in a {
        print(key);}
        return 0; 
        }
    """
source = io.StringIO(abc)
error_manager = ErrorManager()
lexer = Lexer(source, error_manager)
parser = Parser(lexer, error_manager)

program = parser.parse_program()

visitor = ExecuteVisitor()
printerVisitor = PrintVisitor()
interpreter = Interpreter(program)
printerVisitor.visit_program(program)
result = interpreter.execute(visitor)
print(result)