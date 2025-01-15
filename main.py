from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import AndExpression, Assignment, Block, BoolType, DivExpression, EqualityOperation, FloatType, ForEachStatement, FunctionArguments, FunctionCall, Identifier, IntegerType, IntegerValue, LessOperation, MatchCase, MulExpression, Negation, ObjectAccess, Parameter, FunctionDefintion, Program, StringType, StringValue, SumExpression, TypeExpression, TypeMatch
from src.lexer.tokens import TokenType, Token
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, LeadingZeroError,NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
from src.interpreter.print_visitor import PrintVisitor
from src.interpreter.interpreter import Interpreter
from src.interpreter.execute_visitor import ExecuteVisitor
import sys
import io



def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as file:
                source = io.StringIO(file.read())
                error_manager = ErrorManager()
                lexer = Lexer(source, error_manager)
                parser = Parser(lexer, error_manager)
                visitor = ExecuteVisitor()
                printerVisitor = PrintVisitor()
                interpreter = Interpreter(parser.parse_program())
                printerVisitor.visit_program(interpreter.program)
                result = interpreter.execute(visitor)
                print(result)
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku '{file_path}'. Proszę sprawdzić ścieżkę i spróbować ponownie.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
    else:
        print("Proszę uruchomić skrypt z podaniem ścieżki do pliku jako argumentu.")
        print("Przykład:")
        print("python nazwa_skryptu.py ścieżka/do/pliku")

if __name__ == "__main__":
    main()