from src.lexer.tokens import TokenType, Symbols, Token
from src.errors.parser_errors import DictionaryEntriesError, DictionaryEntryError, ExpectedElseBlockOfStatements, ExpectedForEachBlockOfStatements, ExpectedIfBlockOfStatements, ExpectedWhileBlockOfStatements, InvalidAndExpression, InvalidArithmeticExpression, InvalidExpression, InvalidLogicExpression, InvalidOrExpression, InvalidWhileCondition, NoArgumentExpression, NoIfCondition, UnexpectedToken, BuildingFunctionError, SameParameterError, InvalidParameterError, EmptyBlockOfStatements
from src.parser.objects import AndExpression, Block, BoolValue, Dictionary, DictionaryEntry, DivExpression, EqualityOperation, FloatValue, ForEachStatement, FunctionCall, GreaterEqualOperation, GreaterOperation, Identifier ,IfStatement, IntegerValue, LessEqualOperation, LessOperation, MulExpression, Negation, NotEqualOperation, ObjectAccess, OrExpression, Program, FunctionDefintion, Parameter, RelationalExpression, ReturnStatement, StringValue, SubExpression, SumExpression, TypeExpression, WhileStatement
from typing import Optional
import io

class Parser:
    def __init__(self, lexer, error_manager):
        self.lexer = lexer
        self.current_token = None
        self.error_manager = error_manager
        self._get_next_token()

        self.ARTH_OPERATORS = {
            TokenType.PLUS: SumExpression,
            TokenType.MINUS: SubExpression
        }

        self.MUL_OPERATORS = {
            TokenType.MULTIPLY: MulExpression,
            TokenType.DIVIDE: DivExpression
        }

        self.BOOL = {
            TokenType.TRUE,
            TokenType.FALSE
        }

        self.LOGIC_OPERATIONS_MAPPING = {
            TokenType.EQUALS: EqualityOperation,
            TokenType.NOT_EQUALS: NotEqualOperation,
            TokenType.GREATER_THAN: GreaterOperation,
            TokenType.GREATER_THAN_EQUAL: GreaterEqualOperation,
            TokenType.LESS_THAN: LessOperation,
            TokenType.LESS_THAN_EQUAL: LessEqualOperation,
            }
    
    


    def _get_next_token(self):
        self.current_token = self.lexer.get_next_token()

    def raise_exception(self):
        raise SyntaxError()

    def _consume(self, token_type):
        if self.current_token.type == token_type:
            self._get_next_token()
        else:
            raise SyntaxError(f"Oczekiwano tokenu {token_type}, otrzymano {self.current_token.type}")

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
        params = self.parse_parameters()
        self.must_be(TokenType.RPAREN)
        block_statements = self.parse_block()
        return FunctionDefintion(position, type, name, params, block_statements)


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
        if self.try_consume(TokenType.ELSE):
            if not (else_block := self.parse_block()):
                error = ExpectedElseBlockOfStatements(self.current_token)
                self.error_manager.add_parser_error(error)
                raise ExpectedElseBlockOfStatements(self.current_token)
        return IfStatement(position, condition, if_block, else_block)
    
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
    
    # return_statement ::= "return", [ expression ], ";" ;
    def parse_return_statement(self):
        position = self.current_token.position
        if not self.try_consume(TokenType.RETURN):
            return None
        expr = self.parse_or_expression()
        self.must_be(TokenType.SEMICOLON)
        return ReturnStatement(position, expr)
    
    # obj_access ::= item, { ".", function_call } ;
    def parse_object_access(self):
        position = self.current_token.position

        if (item := self.parse_identifier_or_function_call()) == None:
            return None

        function_calls = []

        while self.try_consume(TokenType.DOT):
            function_call = self.parse_identifier_or_function_call()
            if function_call is None:
                error = UnexpectedToken(self.current_token.position, self.current_token.value)
                self.error_manager.add_parser_error(error)
                raise UnexpectedToken(self.current_token.position, self.current_token.value)
            function_calls.append(function_call)

        current_item = item
        if len(function_calls) > 0:
            current_item = ObjectAccess(position, item, function_calls)

        return current_item

    # identifier_or_function_call ::= identifier, [ "(", [ arguments ], ")" ] ; 
    def parse_identifier_or_function_call(self):
        position = self.current_token.position
        if (identifier := self.parse_identifier()) == None:
            return None

        if not self.try_consume(TokenType.LPAREN):
            return identifier
        else:
            arguments = self.parse_arguments()
            self.must_be(TokenType.RPAREN)
            return FunctionCall(position, identifier, arguments)
    
    # arguments ::= expression, { ",", expression } ;
    def parse_arguments(self):
        argumentsList = []
        if (argument := self.parse_expression()) == None:
            return None
        
        argumentsList.append(argument)

        while self.try_consume(TokenType.COMMA):
            if not (argument := self.parse_expression()):
                error = NoArgumentExpression(self.current_token)
                self.error_manager.add_parser_error(error)
                raise NoArgumentExpression(self.current_token)
            argumentsList.append(argument)
        return argumentsList

    # or_expression ::= and_expression, { "||", and_expression } ;
    def parse_or_expression(self):
        position = self.current_token.position
        if not (and_expr := self.parse_and_expression()):
            return None
        expressions = [and_expr]
        while self.try_consume(TokenType.LOGICAL_OR):
            if not (expr := self.parse_and_expression()):
                error = InvalidOrExpression(self.current_token)
                self.error_manager.add_parser_error(error)
                raise InvalidOrExpression(self.current_token)
            expressions.append(expr)
        if len(expressions) == 1:
            return and_expr
        return OrExpression(position, expressions)
     
    # and_expression ::= equality_expression, { "&&", equality_expression } ;
    def parse_and_expression(self):
        position = self.current_token.position
        if not (eq_expr := self.parse_equality_expression()):
            return None
        expressions = [eq_expr]
        while self.try_consume(TokenType.LOGICAL_AND):
            if not (expr := self.parse_equality_expression()):
                error = InvalidAndExpression(self.current_token)
                self.error_manager.add_parser_error(error)
                raise InvalidAndExpression(self.current_token)
            expressions.append(expr)
        if len(expressions) == 1:
            return eq_expr
        return AndExpression(position, expressions)
    
    # equality_expression ::= relational_expression, [ "==" | "!=", relational_expression ] ;
    def parse_equality_expression(self):
        position = self.current_token.position
        if not (rel_expr := self.parse_relational_expression()):
            return None
        if expression_type := self.LOGIC_OPERATIONS_MAPPING.get(self.current_token.type):
            self.consume_token()
            if not (second_rel_expr := self.parse_relational_expression()):
                error = InvalidLogicExpression(self.current_token)
                self.error_manager.add_parser_error(error)
                raise InvalidLogicExpression(self.current_token)
            return expression_type(position, rel_expr, second_rel_expr)
        return rel_expr
       
    # relational_expression ::= add_expression, [ "<" | ">" | "<=" | ">=", add_expression ] ;
    def parse_relational_expression(self):
        position = self.current_token.position
        if not (add_expr := self.parse_add_expression()):
            return None
        if expression_object := self.LOGIC_OPERATIONS_MAPPING.get(self.current_token.type):
            self.consume_token()
            if not (second_add_expr := self.parse_add_expression()):
                error = InvalidLogicExpression(self.current_token)
                self.error_manager.add_parser_error(error)
                raise InvalidLogicExpression(self.current_token)
            return expression_object(position, add_expr, second_add_expr)
        return add_expr
    
    # add_expression ::= mul_expression, { "+" | "-", mul_expression } ;
    def parse_add_expression(self):
        position = self.current_token.position
        if not (mul_expr := self.parse_multiplication_expression()):
            return None
        expressions = [mul_expr]
        while expression_type := self.MUL_OPERATORS.get(self.current_token.type):
            self.consume_token()
            if not (expr := self.parse_multiplication_expresstion()):
                error = InvalidArithmeticExpression(self.current_token)
                self.error_manager.add_parser_error(error)
                raise InvalidArithmeticExpression(self.current_token)
            expressions.append(expr)
        if len(expressions) == 1:
            return mul_expr
        return expression_type(position, expressions)
    
    # mul_expression ::= unary_expression, { "*" | "/", unary_expression } ;
    # def parse_multiplication_expression(self):
    #     position = self.current_token.position
    #     if not (unary_expr := self.parse_unary_expression()):
    #         return None
    #     expressions = [unary_expr]
    #     while expression_type := self.MUL_OPERATORS.get(self.current_token.type):
    #         type = expression_type
    #         self.consume_token()
    #         if not (expr := self.parse_unary_expression()):
    #             error = InvalidArithmeticExpression(self.current_token)
    #             self.error_manager.add_parser_error(error)
    #             raise InvalidArithmeticExpression(self.current_token)
    #         expressions.append(expr)
    #     if len(expressions) == 1:
    #         return unary_expr
    #     return type(position, expressions)
    

    def parse_multiplication_expression(self):
        position = self.current_token.position
        if not (unary_expr := self.parse_unary_expression()):
            return None
        expressions = []
        next_expr = None
        while creator := self.MUL_OPERATORS.get(self.current_token.type):
            self.consume_token()
            if next_expr:
                unary_expr = next_expr
            if next_expr := self.parse_unary_expression():
                a = creator(self.current_token.position, unary_expr, next_expr)
                expressions.append(creator(self.current_token.position, unary_expr, next_expr))
            else:
                raise InvalidArithmeticExpression(self.current_token)
        if len(expressions) == 1:
            return unary_expr                     
        return expressions

    
    # 
    
    # unary_expression ::= [ "-" | "not" | "!" ], type_expression ;
    def parse_unary_expression(self):
        position = self.current_token.position
        if self.current_token.value in ["-", "not", "!"]:
            self.consume_token()
            if not (expr := self.parse_type_expression()):
                error = InvalidArithmeticExpression(self.current_token)
                self.error_manager.add_parser_error(error)
                raise InvalidArithmeticExpression(self.current_token)
            return Negation(position, expr)
        if not (type_expr := self.parse_type_expression()):
            return None
        return type_expr

    
    # type_expression ::= factor, [ "is", type ] ;
    def parse_type_expression(self):
        position = self.current_token.position
        if not (factor := self.parse_factor()):
            return None
        if self.try_consume(TokenType.IS):
            if not (type := self.parse_type()):
                error = InvalidArithmeticExpression(self.current_token)
                self.error_manager.add_parser_error(error)
                raise InvalidArithmeticExpression(self.current_token)   
            return TypeExpression(position, factor, type)
        return factor
        
    # factor ::= literal | "(", expression, ")", | obj_access ;
    def parse_factor(self):
        if obj_access := self.parse_object_access():
            return obj_access
        if self.try_consume(TokenType.LPAREN):
            if not (expression := self.parse_or_expression()):
                error = InvalidExpression(self.current_token)
                self.error_manager.add_parser_error(error)
                raise InvalidExpression(self.current_token) 
            self.must_be(TokenType.RPAREN)
            return expression
        if literal := self.parse_literal():
            return literal
        return None
    
    # expression ::= or_expression ;
    # def parse_expression(self):
    #     if self.try_consume(TokenType.LPAREN):
    #         if not (expression := self.parse_or_expression()):
    #             error = InvalidExpression(self.current_token)
    #             self.error_manager.add_parser_error(error)
    #             raise InvalidExpression(self.current_token) 
    #         self.must_be(TokenType.RPAREN)
    #         return expression
    #     return None


    # literal ::= integer | float | bool | string | dictionary;
    def parse_literal(self):
        variable_value = \
            self.parse_bool()    \
            or self.parse_integer()  \
            or self.parse_float()   \
            or self.parse_string()  \
            # or self.parse_dictionary()
        if variable_value:
            return variable_value
        return None
    
    # LiteralBool i value
    def parse_bool(self):
        position = self.current_token.position
        if (token := self.try_consume(self.BOOL)) == None:
            return None
        if token.type == TokenType.TRUE:
            return BoolValue(position, True)
        return BoolValue(position, False)

    def parse_integer(self):
        position = self.current_token.position
        if (token := self.try_consume(TokenType.INTEGER_VALUE)) == None:
            return None
        return IntegerValue(position, token.value)

    def parse_float(self):
        position = self.current_token.position
        if (token := self.try_consume(TokenType.FLOAT_VALUE)) == None:
            return None
        return FloatValue(position, token.value)

    def parse_string(self):
        position = self.current_token.position
        if (token := self.try_consume(TokenType.STRING_VALUE)) == None:
            return None
        return StringValue(position, token.value)
    
    # dictionary ::= "{", [ dict_entries ], "}" ;
    def parse_dictionary(self):
        position = self.current_token.position
        if self.try_consume(TokenType.LBRACE) == None:
            return None
        if not (dictionary_entries := self.parse_dictionary_entries()):
                error = DictionaryEntriesError(self.current_token)
                self.error_manager.add_parser_error(error)
                raise DictionaryEntriesError(self.current_token) 
        self.must_be(TokenType.RBRACE)
        return Dictionary(position, dictionary_entries)


    # dictionary ::= "{", [ dict_entries ], "}" ;
    def parse_dictionary_entries(self):
        position = self.current_token.position
        if not (entry := self.parse_dictionary_entry()):
            return None
        entries = [entry]
        while self.try_consume(TokenType.COMMA):
            if not (entry := self.parse_dictionary_entry()):
                error = DictionaryEntriesError(self.current_token)
                self.error_manager.add_parser_error(error)
                raise DictionaryEntriesError(self.current_token) 
            entries.append(entry)
        return entries
            


    
    def parse_dictionary_entry(self):
        position = self.current_token.position
        if not (expression := self.parse_or_expression()):
            return None
        self.must_be(TokenType.SEMICOLON)
        if not (expression2 := self.parse_or_expression()):
            error = DictionaryEntryError(self.current_token)
            self.error_manager.add_parser_error(error)
            raise DictionaryEntryError(self.current_token)
        return  DictionaryEntry(position, expression, expression2)
        



        # if self.try_consume(TokenType.LBRACE) == None:
        #     return None
        # if not (dictionary_entries := self.parse_dictionary_entries()):
        #         error = DictionaryEntriesError(self.current_token)
        #         self.error_manager.add_parser_error(error)
        #         raise DictionaryEntriesError(self.current_token) 
        # self.must_be(TokenType.RBRACE)
        # return Dictionary(position, dictionary_entries)



# parameters ::= parameter, { ",", parameter } ;
    def parse_parameters(self):
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
        position = self.current_token.position
        if (token_type := self.parse_type_or_varinat()) == None:
            return None
        if param := self.try_consume(TokenType.IDENTIFIER):
            return Parameter(position, token_type, param.value)
        return None
    

    def parse_type_or_varinat(self):
        token = self.current_token
        if token_type := self.parse_type():
            return token_type
        elif token.type == TokenType.VARIANT:
            self.consume_token()
            return token.value
        else:
            return None
    

    def parse_type(self):
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


    def _try_parse_type(self) -> Optional[str]:
        lexerToken = self.__get_current_token()
        if lexerToken.value in ["int", "float", "frc", "string"]:
            self.__get_next_token()
            return lexerToken.value
        else:
            return None