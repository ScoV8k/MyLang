from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import AndExpression, Assignment, Block, BoolType, DivExpression, EqualityOperation, FloatType, ForEachStatement, FunctionArguments, FunctionCall, Identifier, IntegerType, IntegerValue, LessOperation, MatchCase, MulExpression, Negation, ObjectAccess, Parameter, FunctionDefintion, Program, StringType, StringValue, SumExpression, TypeExpression, TypeMatch
from src.lexer.tokens import TokenType, Token
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, LeadingZeroError,NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
# from src.interpreter.visitor import Visitor
from src.interpreter.print_visitor import PrintVisitor
from src.interpreter.interpreter import Interpreter
from src.interpreter.ex_vis import ExecuteVisitor
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
source = io.StringIO(source_code)
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