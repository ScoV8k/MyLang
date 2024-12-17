from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.objects import AndExpression, Assignment, Block, BoolType, DivExpression, EqualityOperation, FloatType, ForEachStatement, FunctionArguments, FunctionCall, Identifier, IntegerType, IntegerValue, LessOperation, MatchCase, MulExpression, Negation, ObjectAccess, Parameter, FunctionDefintion, Program, StringType, StringValue, SumExpression, TypeExpression, TypeMatch
# from src.lexer.source import String, File
from src.lexer.tokens import TokenType, Token
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, IdentifierTooLongError, LeadingZeroError,NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
import sys
import io




# source_code = "int main() {for each (key, value) in myDict { doSomething(); }}"
# source = io.StringIO(source_code)
# error_manager = ErrorManager()
# lexer = Lexer(source, error_manager)
# parser = Parser(lexer, error_manager)

# program = parser.parse_program()
# print(program)
# expected_key = "key"
# expected_value = "value"
# expected_expr = Identifier((1, 38), "myDict")
# expected_block1 = Block((1, 45), [
#     FunctionCall((1, 47), "doSomething", None)
# ])
# integer_type = IntegerType((1, 1), 'int')
# expected_for_each = ForEachStatement((1, 13), expected_key, expected_value, expected_expr, expected_block1)
# expected_block2 = Block((1, 12), [expected_for_each])
# expected_function_def = FunctionDefintion((1, 1), integer_type, 'main', [], expected_block2)
# expected_program = Program((1, 1), [expected_function_def])

# print(expected_program)

# print("\n\n\n\n")

# print(program)