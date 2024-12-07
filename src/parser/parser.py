from src.lexer.tokens import TokenType, Symbols, Token
from src.errors.parser_errors import ExpectedElseBlockOfStatements, ExpectedForEachBlockOfStatements, ExpectedIfBlockOfStatements, ExpectedWhileBlockOfStatements, InvalidWhileCondition, NoIfCondition, UnexpectedToken, BuildingFunctionError, SameParameterError, InvalidParameterError, EmptyBlockOfStatements
from src.parser.objects import Block, ForEachStatement, FunctionCall, Identifier ,IfStatement, Program, FunctionDefintion, Parameter, ReturnStatement, WhileStatement, Blockś
from typing import Optional
import io

class Parser:
    def __init__(self, lexer, error_manager):
        self.lexer = lexer
        self.current_token = None
        self.error_manager = error_manager
        self._get_next_token()

    def _get_next_token(self):
        """Przesuń do następnego tokena."""
        self.current_token = self.lexer.get_next_token()

    def raise_exception(self, token_type):
        raise SyntaxError() #currentTokenType na tekst?

    def _consume(self, token_type):
        if self.current_token.type == token_type:
            self._get_next_token()
        else:
            raise SyntaxError(f"Expected token {token_type}, but got {self.current_token.type}")

    def consume_token(self):
        self.current_token = self.lexer.get_next_token()
        if self.current_token.type == TokenType.COMMENT:
            self.consume_token()
    
    def check_token_type(self, type) -> bool:
        if isinstance(type, TokenType):
            type = {type}
        return self.current_token.type in type

    def try_consume(self, types):
        if not self.check_token_type(types):
           return None
        token = self.current_token
        self.consume_token()
        return token
    
    def must_be(self, types):
        if not self.check_token_type(types):
           self.raise_exception(types)
        token = self.current_token
        self.consume_token()
        return token
    

    def parse(self):
        return self._parse_expression()
    
    def parse_program(self):
        # functions = self.parse_function_definition()
        position = self.current_token.position
        functions = []

        while fun := self.parse_function_definition():
            functions.append(fun)
        if self.current_token.type is not TokenType.EOF:
            error = UnexpectedToken(self.current_token.position, self.current_token.value)
            self.error_manager.add_parser_error(error)
        return Program(position, functions)
    
        # function_definition = "def", function_name, "(", parameters , ")" , statements; 
    def parse_function_definition(self) -> Optional[FunctionDefintion]:
        if self.current_token.type not in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.DICT, TokenType.BOOL, TokenType.VOID]:
            return None
        position = self.current_token.position
        type = self.current_token.type
        # self.lexer.get_next_token()
        self.consume_token()
        if self.current_token.type != TokenType.IDENTIFIER:
            self.error_manager.add_parser_error(BuildingFunctionError(position, self.current_token))
            raise BuildingFunctionError(position, self.current_token)
        name = self.current_token.value
        # self.lexer.get_next_token()
        self.consume_token()
        self.must_be(TokenType.LPAREN)
        params = self._parse_parameters()
        self.must_be(TokenType.RPAREN)
        self.must_be(TokenType.LBRACE)
        block_statements = self.parse_block()
        self.must_be(TokenType.RBRACE)
        # if not block_statements:
        #     ExpectedBlockStatements(self.current_token, 'Expected block statements in function definition')
        return FunctionDefintion(position, name, params, block_statements)


    # block ::= "{", { block_statement }, "}" ;
    def parse_block(self):
        if not self.try_consume(TokenType.LBRACE): 
            return None
        position = self.current_token.position
        statements = []
        while statement := self.parse_statement():
            statements.append(statement)
        self.must_be(TokenType.RBRACE)
        if len(statements) == 0:
            raise EmptyBlockOfStatements(position, self.current_token)
        return Block(position, statements)
        
    # block_statement ::= declaration | assignment | if_statement | while_loop | for_each_loop| type_match | return_statement ;
    def parse_statement(self):
        if statement := \
            self.parse_declaration() \
            or self.parse_assignment() \
            or self.parse_if_statement() \
            or self.parse_while_loop() \
            or self.parse_for_each_loop() \
            or self.parse_type_match() \
            or self.parse_return_statement():
            return statement
        return None


   # if_statement ::= "if", "(", expression, ")", block, [ "else", block ] ;
    def parse_if_statement(self):
        if not self.try_consume(TokenType.IF):
            return None
        position = self.current_token.position
        self.must_be(TokenType.LPAREN)
        if not (condition := self.parse_or_expression()):
            error = NoIfCondition(self.current_token)
            self.error_manager.add_parser_error(error)
            raise NoIfCondition(self.current_token)
        self.must_be(TokenType.RPAREN)
        if not (if_block := self.parse_block()):
            error = ExpectedIfBlockOfStatements(self.current_token)
            self.error_manager.add_parser_error(error)
            ExpectedIfBlockOfStatements(self.current_token)
        else_statements = None
        if self.try_consume(TokenType.ELSE):
            if not (else_block := self.parse_block()):
                error = ExpectedElseBlockOfStatements(self.current_token)
                self.error_manager.add_parser_error(error)
                raise ExpectedElseBlockOfStatements(self.current_token)
        return IfStatement(position, condition, if_block, else_block)
    
    #while = "while", "(", expression, ")", statements; 
    #while_loop ::= "while", "(", expression, ")", block ;
    def parse_while_loop(self):
        if self.try_consume(TokenType.WHILE):
            position = self.current_token.position
            self.must_be(TokenType.LPAREN)
            if not (while_condition := self.parse_or_expression()):
                error = InvalidWhileCondition(self.current_token)
                self.error_manager.add_parser_error(error)
                raise InvalidWhileCondition(self.current_token)
            self.must_be(TokenType.RPAREN)
            if not (while_block := self.parse_block()):
                error = ExpectedWhileBlockOfStatements(self.current_token)
                self.error_manager.add_parser_error(error)
                ExpectedWhileBlockOfStatements(self.current_token)
            return WhileStatement(position, while_condition, while_block)
        return None
    
    # for_each_loop ::= "for", "each", "(", identifier, ",", identifier, ")", "in", identifier, block ;
    def parse_for_each_loop(self):
        if self.try_consume(TokenType.FOR):
            position = self._consume.position
            self.must_be(TokenType.EACH)
            self.must_be(TokenType.LPAREN)
            key = self.must_be(TokenType.IDENTIFIER).value
            self.must_be(TokenType.COMMA)
            value = self.must_be(TokenType.IDENTIFIER).value
            self.must_be(TokenType.RPAREN)
            self.must_be(TokenType.IN)
            struct = self.must_be(TokenType.IDENTIFIER).value
            if not (for_each_block := self.parse_block()):
                error = ExpectedForEachBlockOfStatements(self.current_token)
                self.error_manager.add_parser_error(error)
                ExpectedForEachBlockOfStatements(self.current_token)
            return ForEachStatement(position, key, value, struct, for_each_block)
        return None
    
    def parse_return_statement(self):
        position = self.current_token.position
        if not self.try_consume(TokenType.RETURN):
            return None
        expr = self.parse_or_expression()
        self.must_be(TokenType.SEMICOLON)
        return ReturnStatement(position, expr)
    

    # SPRAWDZIĆ BO MAM WRAZENIE ZE COS NA 100% JEST ŹLE
    def parse_function_call_or_identifier(self):
        if (identifier := self.parse_identifier()) == None:
            return None

        if not self.try_consume(TokenType.LPAREN):
            return identifier
        else:
            arguments = self.try_parse_arguments()
            self.must_be(TokenType.RPAREN)
            return FunctionCall(identifier, arguments)
    

# parameters ::= parameter, { ",", parameter } ;
    def _parse_parameters(self):
        params = []
        if (param := self.parse_parameter()) == None:
            return params
        params.append(param)
        while self.try_consume(TokenType.COMMA):
            if not (param := self.parse_parameter()):
                self.error_manager.add_parser_error(InvalidParameterError(self.current_token.position))
                raise InvalidParameterError(self.current_token)
            elif param in params:
                raise SameParameterError(self.current_token.position, param)
            else:
                params.append(param)
        return params

# parameter ::= type_or_variant, identifier ;
    def parse_parameter(self):
        # if self.current_token.type not in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.DICT, TokenType.BOOL, TokenType.VARIANT]:
        #     return None
        if (token_type := self._parse_type_or_varinat()) == None:
            return None
        position = self.current_token.position
        if param := self.try_consume(TokenType.IDENTIFIER):
            return Parameter(position, token_type, param.value)
        return None
    

    def _parse_type_or_varinat(self):
        token = self.current_token
        if token_type := self._parse_type():
            return token_type
        elif token.type == TokenType.VARIANT:
            self.consume_token()
            return token.value
        else:
            return None
    

    def _parse_type(self):
        token = self.current_token
        if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING, TokenType.DICT]:
            self.consume_token()
            return token.value
        else:
            return None
    
    def parse_identifier(self):
            if not (token := self.try_consume(TokenType.IDENTIFIER)):
                return None
            else:
                return Identifier(token.position, token.value)


    def _parse_expression(self):
        """
        Parsuj wyrażenie:
        expression -> term (("+" | "-") term)*
        """
        node = self._parse_term()
        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            self._get_next_token()
            node = {
                "type": "BinaryOperation",
                "operator": token.value,
                "left": node,
                "right": self._parse_term(),
            }
        return node

    def _parse_term(self):
        """
        Parsuj czynnik:
        term -> factor (("*" | "/") factor)*
        """
        node = self._parse_factor()
        while self.current_token and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            self._get_next_token()
            node = {
                "type": "BinaryOperation",
                "operator": token.value,
                "left": node,
                "right": self._parse_factor(),
            }
        return node

    def _parse_factor(self):
        """
        Parsuj czynnik:
        factor -> NUMBER | "(" expression ")"
        """
        token = self.current_token
        if token.type == TokenType.INTEGER_VALUE or token.type == TokenType.FLOAT_VALUE:
            self._get_next_token()
            return {"type": "Number", "value": token.value}

        elif token.type == TokenType.LEFT_PAREN:
            self._get_next_token()
            node = self._parse_expression()
            self._consume(TokenType.RIGHT_PAREN)
            return node

        else:
            raise SyntaxError(f"Unexpected token: {token.type}")


    def _try_parse_type(self) -> Optional[str]:
        lexerToken = self.__get_current_token()
        if lexerToken.value in ["int", "float", "frc", "string"]:
            self.__get_next_token()
            return lexerToken.value
        else:
            return None