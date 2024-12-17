from src.lexer.tokens import TokenType, Symbols, Token
from src.errors.parser_errors import DictionaryEntriesError, DictionaryEntryError, ExpectedElseBlockOfStatements, ExpectedForEachBlockOfStatements, ExpectedIfBlockOfStatements, ExpectedWhileBlockOfStatements, InvalidAddExpression, InvalidAndExpression, InvalidArithmeticExpression, InvalidExpression, InvalidLogicExpression, InvalidMultiplicationExpression, InvalidOrExpression, InvalidWhileCondition, NoArgumentExpression, NoBlockInMatchCaseError, NoIdentifierAfterAs, NoIfCondition, NoTypeMatchExpressionError, UnexpectedToken, BuildingFunctionError, SameParameterError, InvalidParameterError, EmptyBlockOfStatements
from src.parser.objects import AndExpression, Assignment, Block, BoolValue, Dictionary, DictionaryEntry, DivExpression, EqualityOperation, FloatValue, ForEachStatement, FunctionCall, GreaterEqualOperation, GreaterOperation, Identifier ,IfStatement, IntegerType, IntegerValue, LessEqualOperation, LessOperation, MatchCase, MulExpression, Negation, NotEqualOperation, ObjectAccess, OrExpression, Program, FunctionDefintion, Parameter, RelationalExpression, ReturnStatement, StringValue, SubExpression, SumExpression, TypeExpression, TypeMatch, WhileStatement
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
        
        self.TYPE_MAPPING = {
            TokenType.INT: IntegerType
            # TokenType.FLOAT: FloatType,
            # TokenType.BOOL: BoolType,
            # TokenType.STRING: StringType,
            # TokenType.DICT: DictType,
            # TokenType.VARIANT: VariantType,
            # TokenType.VOID: VoidType
        }
    
    


    def _get_next_token(self):
        self.current_token = self.lexer.get_next_token()
        while self.current_token.type == TokenType.COMMENT:
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

    
    def check_token_type(self, type):
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

    
    def parse_program(self):
        position = self.current_token.position
        functions = []

        while fun := self.parse_function_definition():
            functions.append(fun)
        if self.current_token.type is not TokenType.EOF:
            error = UnexpectedToken(self.current_token.position, self.current_token.value)
            self.error_manager.add_parser_error(error)
        return Program(position, functions)
    
    # function_def ::= func_type, identifier, "(", [ parameters ], ")", block ;
    def parse_function_definition(self) -> Optional[FunctionDefintion]:
        if self.current_token.type not in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.DICT, TokenType.BOOL, TokenType.VOID, TokenType.VARIANT]:
            return None
        position = self.current_token.position
        type = self.current_token.type
        self.consume_token()
        if self.current_token.type != TokenType.IDENTIFIER:
            raise BuildingFunctionError(position, self.current_token)
        name = self.current_token.value
        self.consume_token()
        self.must_be(TokenType.LPAREN)
        params = self.parse_parameters()
        self.must_be(TokenType.RPAREN)
        if not( block_statements := self.parse_block()):
            raise BuildingFunctionError(position, self.current_token) # DODAC ERROR
        return FunctionDefintion(position, type, name, params, block_statements)


    # block ::= "{", { block_statement }, "}" ;
    def parse_block(self):
        position = self.current_token.position
        if not self.try_consume(TokenType.LBRACE): 
            return None
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

    # declaration ::= parameter, [ "=", expression ], ";" ;
    def parse_declaration(self):
        position = self.current_token.position
        if (obj_access := self.parse_parameter()) == None:
            return None
        if self.try_consume(TokenType.ASSIGN):
            if not (expression := self.parse_or_expression()):
                raise NoIfCondition(self.current_token) #TODO
        self.must_be(TokenType.SEMICOLON)
        return Assignment(position, obj_access, expression)


    # assignment ::= obj_access, [ "=", expression ], ";" ;
    def parse_assignment(self):
        position = self.current_token.position
        if (statement := self.parse_object_access()) == None:
            return None
        expression = None
        if self.try_consume(TokenType.ASSIGN):
            if not (expression := self.parse_or_expression()):
                raise NoIfCondition(self.current_token) #TODO
            statement = Assignment(position, statement, expression)
        self.must_be(TokenType.SEMICOLON)
        return statement
    

    # type_match ::= "match", expression, [ "as", identifier ], "{", { match_case }, "}" ; 
    def parse_type_match(self):
        position = self.current_token.position
        if not self.try_consume(TokenType.MATCH):
            return None
        if not (expression := self.parse_or_expression()):
                raise NoTypeMatchExpressionError(self.current_token)
        identifier = None
        if self.try_consume(TokenType.AS):
            if not (identifier := self.try_consume(TokenType.IDENTIFIER)):
                raise NoIdentifierAfterAs(self.current_token)
            identifier = identifier.value
        self.must_be(TokenType.LBRACE)
        cases = []
        while match_case := self.parse_match_case():
            cases.append(match_case)
        self.must_be(TokenType.RBRACE)
        return TypeMatch(position, expression, cases, identifier)

    # match_case ::= type, "=>", block | "null", "=>", block | "_", "=>", block ;
    def parse_match_case(self):
        position = self.current_token.position
        if self.try_consume(TokenType.NULL):
            type = "null"
        elif self.try_consume(TokenType.UNDERSCORE):
            type = "_"
        else:
            if not (type := self.parse_type()):
                return None
        self.must_be(TokenType.ARROW)
        if not (block := self.parse_block()):
            raise NoBlockInMatchCaseError(position, self.current_token)
        return MatchCase(position, type, block)
            


   # if_statement ::= "if", "(", expression, ")", block, [ "else", block ] ;
    def parse_if_statement(self):
        if not self.try_consume(TokenType.IF):
            return None
        position = self.current_token.position
        self.must_be(TokenType.LPAREN)
        if not (condition := self.parse_or_expression()):
            raise NoIfCondition(self.current_token)
        self.must_be(TokenType.RPAREN)
        if not (if_block := self.parse_block()):
            ExpectedIfBlockOfStatements(self.current_token)
        if self.try_consume(TokenType.ELSE):
            if not (else_block := self.parse_block()):
                raise ExpectedElseBlockOfStatements(self.current_token)
        return IfStatement(position, condition, if_block, else_block)
    
    #while_loop ::= "while", "(", expression, ")", block ;
    def parse_while_loop(self):
        if self.try_consume(TokenType.WHILE):
            position = self.current_token.position
            self.must_be(TokenType.LPAREN)
            if not (while_condition := self.parse_or_expression()):
                raise InvalidWhileCondition(self.current_token)
            self.must_be(TokenType.RPAREN)
            if not (while_block := self.parse_block()):
                raise ExpectedWhileBlockOfStatements(self.current_token)
            return WhileStatement(position, while_condition, while_block)
        return None
    
    # for_each_loop ::= "for", "each", "(", identifier, ",", identifier, ")", "in", expression, block ;
    def parse_for_each_loop(self):
        position = self.current_token.position
        if self.try_consume(TokenType.FOR):
            self.must_be(TokenType.EACH)
            self.must_be(TokenType.LPAREN)
            key = self.must_be(TokenType.IDENTIFIER).value
            self.must_be(TokenType.COMMA)
            value = self.must_be(TokenType.IDENTIFIER).value
            self.must_be(TokenType.RPAREN)
            self.must_be(TokenType.IN)
            # struct = self.must_be(TokenType.IDENTIFIER).value
            if not (expr := self.parse_or_expression()):
                raise NoForEachExpression
            if not (for_each_block := self.parse_block()):
                raise ExpectedForEachBlockOfStatements(self.current_token)
            return ForEachStatement(position, key, value, expr, for_each_block)
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
                raise UnexpectedToken(self.current_token.position, self.current_token.value)
            function_calls.append(function_call)

        current_item = item
        if len(function_calls) > 0:
            current_item = ObjectAccess(position, item, function_calls)

        return current_item

    # identifier_or_function_call ::= identifier, [ "(", [ arguments ], ")" ] ; 
    def parse_identifier_or_function_call(self):
        position = self.current_token.position
        if (identifier := self.try_consume(TokenType.IDENTIFIER)) == None:
            return None
        if not self.try_consume(TokenType.LPAREN):
            return Identifier(identifier.position, identifier.value)
        else:
            arguments = self.parse_arguments()
            self.must_be(TokenType.RPAREN)
            return FunctionCall(position, identifier.value, arguments)
    
    # arguments ::= expression, { ",", expression } ;
    def parse_arguments(self):
        argumentsList = []
        if (argument := self.parse_or_expression()) == None:
            return None
        
        argumentsList.append(argument)

        while self.try_consume(TokenType.COMMA):
            if not (argument := self.parse_expression()):
                raise NoArgumentExpression(self.current_token)
            argumentsList.append(argument)
        return argumentsList

    # or_expression ::= and_expression, { "||", and_expression } ;
    def parse_or_expression(self):
        position = self.current_token.position
        if not (left := self.parse_and_expression()):
            return None
        expressions = [left]
        while self.try_consume(TokenType.LOGICAL_OR):
            if not (right := self.parse_and_expression()):
                raise InvalidOrExpression(self.current_token)
            expressions.append(right)
        if len(expressions) == 1:
            return left
        return OrExpression(position, expressions)

     
    # and_expression ::= equality_expression, { "&&", equality_expression } ;
    def parse_and_expression(self):
        position = self.current_token.position
        if not (left := self.parse_equality_expression()):
            return None
        expressions = [left]
        while self.try_consume(TokenType.LOGICAL_AND):
            if not (right := self.parse_equality_expression()):
                raise InvalidAndExpression(self.current_token)
            expressions.append(right)
        if len(expressions) == 1:
            return left
        return AndExpression(position, expressions)
    
    # equality_expression ::= relational_expression, [ "==" | "!=", relational_expression ] ;
    def parse_equality_expression(self):
        position = self.current_token.position
        if not (rel_expr := self.parse_relational_expression()):
            return None
        if expression_type := self.LOGIC_OPERATIONS_MAPPING.get(self.current_token.type):
            self.consume_token()
            if not (second_rel_expr := self.parse_relational_expression()):
                raise InvalidEqualityExpression(self.current_token)
            return expression_type(position, rel_expr, second_rel_expr)
        return rel_expr
       
    # relational_expression ::= add_expression, [ "<" | ">" | "<=" | ">=", add_expression ] ;
    def parse_relational_expression(self):
        position = self.current_token.position
        if not (left := self.parse_add_expression()):
            return None
        if creator := self.LOGIC_OPERATIONS_MAPPING.get(self.current_token.type):
            self.consume_token()
            if not (right := self.parse_add_expression()):
                raise InvalidRelationalExpression(self.current_token)
            return creator(position, left, right)
        return left
    
    # add_expression ::= mul_expression, { "+" | "-", mul_expression } ;
    def parse_add_expression(self):
        position = self.current_token.position
        if not (left := self.parse_multiplication_expression()):
            return None
        while creator := self.ARTH_OPERATORS.get(self.current_token.type):
            self.consume_token()
            if not (right := self.parse_multiplication_expression()):
                raise InvalidAddExpression(self.current_token)
            left = creator(position, left, right)                   
        return left
    


    # mul_expression ::= unary_expression, { "*" | "/", unary_expression } ;
    def parse_multiplication_expression(self):
        position = self.current_token.position
        if not (left := self.parse_unary_expression()):
            return None
        while creator := self.MUL_OPERATORS.get(self.current_token.type):
            self.consume_token()
            if not (right := self.parse_unary_expression()):
                raise InvalidMultiplicationExpression(self.current_token)
            left = creator(position, left, right)                   
        return left

    

    # unary_expression ::= [ "-" | "not" | "!" ], type_expression ;
    def parse_unary_expression(self):
        position = self.current_token.position
        negate = False
        if self.current_token.value in ["-", "not", "!"]:
            negate = True
            self.consume_token()
        if not (type_expr := self.parse_type_expression()):
            return None
        if negate:
            return Negation(position, type_expr)
        return type_expr


    
    # type_expression ::= factor, [ "is", type ] ;
    def parse_type_expression(self):
        position = self.current_token.position
        if not (factor := self.parse_factor()):
            return None
        if self.try_consume(TokenType.IS):
            if not (type := self.parse_type()):
                raise InvalidArithmeticExpression(self.current_token)   
            return TypeExpression(position, factor, type)
        return factor
        
    # factor ::= literal | "(", expression, ")", | obj_access ;
    # def parse_factor(self): # zrobić analogicznie jak parse_literal
    #     if obj_access := self.parse_object_access():
    #         return obj_access
    #     if self.try_consume(TokenType.LPAREN):
    #         if not (expression := self.parse_or_expression()):
    #             raise InvalidExpression(self.current_token) 
    #         self.must_be(TokenType.RPAREN)
    #         return expression
    #     if literal := self.parse_literal():
    #         return literal
    #     return None
    
    # factor ::= literal | "(", expression, ")", | obj_access ;
    def parse_factor(self):
        factor_value = \
            self.parse_object_access() \
            or self.parse_parenthesized_expression() \
            or self.parse_literal() 
        if factor_value:
            return factor_value
        return None

    def parse_parenthesized_expression(self):
        if self.try_consume(TokenType.LPAREN):
            if not (expression := self.parse_or_expression()):
                raise InvalidExpression(self.current_token)
            self.must_be(TokenType.RPAREN)
            return expression
        return None


    # literal ::= integer | float | bool | string | dictionary;
    def parse_literal(self): 
        variable_value = \
            self.parse_bool()    \
            or self.parse_integer()  \
            or self.parse_float()   \
            or self.parse_string()  \
            or self.parse_dictionary()
        if variable_value:
            return variable_value
        return None
    
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
                raise DictionaryEntriesError(self.current_token) 
        self.must_be(TokenType.RBRACE)
        return Dictionary(position, dictionary_entries)


    # dict_entries ::= expression, ":", expression, { ",", expression, ":", expression } ;
    def parse_dictionary_entries(self):
        position = self.current_token.position
        if not (entry := self.parse_dictionary_entry()):
            return None
        entries = [entry]
        while self.try_consume(TokenType.COMMA):
            if not (entry := self.parse_dictionary_entry()):
                raise DictionaryEntriesError(self.current_token) 
            entries.append(entry)
        return entries
            
    
    def parse_dictionary_entry(self):
        position = self.current_token.position
        if not (expression := self.parse_or_expression()):
            return None
        self.must_be(TokenType.SEMICOLON)
        if not (expression2 := self.parse_or_expression()):
            raise DictionaryEntryError(self.current_token)
        return  DictionaryEntry(position, expression, expression2)
        

    # parameters ::= parameter, { ",", parameter } ;
    def parse_parameters(self):
        params = []
        if (param := self.parse_parameter()) == None:
            return params
        params.append(param)
        while self.try_consume(TokenType.COMMA):
            if not (param := self.parse_parameter()):
                raise InvalidParameterError(self.current_token)
            elif param in params: # porównywanie po samej nazwie parametru param.name
                raise SameParameterError(self.current_token.position, param)
            else:
                params.append(param)
        return params

# parameter ::= type_or_variant, identifier ;
    def parse_parameter(self):
        position = self.current_token.position
        if (token_type := self.parse_type()) == None:
            return None
        if param := self.try_consume(TokenType.IDENTIFIER):
            return Parameter(position, token_type, param.value)
        return None
    

    # def parse_type_or_varinat(self): # Zrobić matcha z mapowaniem na typy
    #     token = self.current_token
    #     if token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING, TokenType.DICT, TokenType.VARIANT]:
    #         self.consume_token()
    #         return token.value
    #     else:
    #         return None
    
    # func_type ::= type | "void";
    def parse_func_type(self):
        token = self.current_token
        if token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING, TokenType.DICT, TokenType.VOID, TokenType.VARIANT]:
            self.consume_token()
            return token.value
        else:
            return None


    # def parse_type(self):
    #     token = self.current_token
    #     if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING, TokenType.DICT, TokenType.VARIANT]:
    #         self.consume_token()
    #         return token.value
    #     else:
    #         return None
    


    def parse_type(self):
        token = self.current_token
        if (type := self.TYPE_MAPPING.get(self.current_token.type)):
            self.consume_token()
            return type(token.position, token.value)
        else:
            return None
    