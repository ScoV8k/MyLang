from src.lexer.tokens import TokenType, Symbols, Token
from src.errors.parser_errors import InvalidTypeExpression, DictionaryEntriesError, DictionaryEntryError, ExpectedElseBlockOfStatements, ExpectedForEachBlockOfStatements, ExpectedIfBlockOfStatements, ExpectedWhileBlockOfStatements, InvalidAddExpression, InvalidAndExpression, InvalidArithmeticExpression, InvalidEqualityExpression, InvalidExpression, InvalidLogicExpression, InvalidMultiplicationExpression, InvalidOrExpression, InvalidRelationalExpression, InvalidWhileCondition, NoArgumentExpression, NoBlockInFunctionDefinition, NoBlockInMatchCaseError, NoExpressionInAssignment, NoExpressionInDeclaration, NoForEachExpression, NoFunctionCallInObjectAccess, NoIdentifierAfterAs, NoIdentifierInDeclaration, NoIfCondition, NoTypeMatchExpressionError, UnexpectedToken, BuildingFunctionError, SameParameterError, InvalidParameterError, EmptyBlockOfStatements, UnexpectedTokenType
from src.parser.objects import NullValue, AndExpression, Declaration, AnyType, Assignment, Block, BoolType, BoolValue, Dictionary, DictionaryEntry, DictionaryType, DivExpression, BreakStatement, EqualityOperation, FloatType, FloatValue, ForEachStatement, FunctionCall, GreaterEqualOperation, GreaterOperation, Identifier ,IfStatement, IntegerType, IntegerValue, LessEqualOperation, LessOperation, MatchCase, MulExpression, Negation, NotEqualOperation, ObjectAccess, OrExpression, Program, FunctionDefintion, Parameter, RelationalExpression, ReturnStatement, StringType, StringValue, SubExpression, SumExpression, TypeExpression, TypeMatch, VariantType, VoidType, WhileStatement
from typing import Optional
import io

class Parser:
    def __init__(self, lexer, error_manager):
        self.lexer = lexer
        self.current_token = None
        self.error_manager = error_manager
        self._get_next_token()

        self.ADDITIVE_OPERATORS = {
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
            TokenType.INT: IntegerType, 
            TokenType.FLOAT: FloatType,
            TokenType.BOOL: BoolType,
            TokenType.STRING: StringType,
            TokenType.DICT: DictionaryType,
            TokenType.VARIANT: VariantType
        }


    def _get_next_token(self):
        self.current_token = self.lexer.get_next_token()
        while self.current_token.type == TokenType.COMMENT:
            self.current_token = self.lexer.get_next_token()

            
    def _consume(self, token_type):
        if self.current_token.type == token_type:
            self._get_next_token()
        else:
            raise UnexpectedTokenType(self.current_token, token_type)

    def _consume_token(self):
        self.current_token = self.lexer.get_next_token()
        while self.current_token.type == TokenType.COMMENT:
            self.current_token = self.lexer.get_next_token()

    
    def _check_token_type(self, type):
        if isinstance(type, TokenType):
            type = {type}
        return self.current_token.type in type

    def _try_consume(self, types):
        if not self._check_token_type(types):
           return None
        token = self.current_token
        self._consume_token()
        return token
    
    def _must_be(self, types):
        if not self._check_token_type(types):
            raise UnexpectedTokenType(self.current_token, types)
        token = self.current_token
        self._consume_token()
        return token

    
    def parse_program(self):
        position = self.current_token.position
        functions = []

        while fun := self._parse_function_definition():
            functions.append(fun)
        if self.current_token.type is not TokenType.EOF:
            raise UnexpectedToken(self.current_token)
        return Program(position, functions)
    
    # function_def ::= func_type, identifier, "(", [ parameters ], ")", block ;
    def _parse_function_definition(self):
        position = self.current_token.position
        if not (type := self._parse_func_type()):
            return None
        if self.current_token.type != TokenType.IDENTIFIER:
            raise BuildingFunctionError(self.current_token)
        name = self.current_token.value
        self._consume_token()
        self._must_be(TokenType.LPAREN)
        params = self._parse_parameters()
        self._must_be(TokenType.RPAREN)
        if not( block_statement := self._parse_block()):
            raise NoBlockInFunctionDefinition(self.current_token)
        return FunctionDefintion(position, type, name, params, block_statement)


    # block ::= "{", { block_statement }, "}" ;
    def _parse_block(self):
        position = self.current_token.position
        if not self._try_consume(TokenType.LBRACE): 
            return None
        statements = []
        while statement := self._parse_statement():
            statements.append(statement)
        self._must_be(TokenType.RBRACE)
        if len(statements) == 0:
            raise EmptyBlockOfStatements(self.current_token)
        return Block(position, statements)
        
    # block_statement ::= declaration | assignment | if_statement | while_loop | for_each_loop| type_match | return_statement ;
    def _parse_statement(self):
        if statement := \
            self._parse_declaration() \
            or self._parse_assignment() \
            or self._parse_if_statement() \
            or self._parse_while_loop() \
            or self._parse_for_each_loop() \
            or self._parse_type_match() \
            or self._parse_break_statement() \
            or self._parse_return_statement():
            return statement
        return None

    # declaration ::= parameter, [ "=", expression ], ";" ;
    def _parse_declaration(self):
        position = self.current_token.position
        if (statement := self._parse_parameter()) == None:
            return None
        if self._try_consume(TokenType.ASSIGN):
            if not (expression := self._parse_or_expression()):
                raise NoExpressionInDeclaration(self.current_token)
            statement = Declaration(position, statement, expression)
        self._must_be(TokenType.SEMICOLON)
        return statement


    # assignment ::= obj_access, [ "=", expression ], ";" ;
    def _parse_assignment(self):
        position = self.current_token.position
        if (statement := self._parse_object_access()) == None:
            return None
        expression = None
        if self._try_consume(TokenType.ASSIGN):
            if not (expression := self._parse_or_expression()):
                raise NoExpressionInAssignment(self.current_token)
            statement = Assignment(position, statement, expression)
        self._must_be(TokenType.SEMICOLON)
        return statement
    

    # type_match ::= "match", expression, [ "as", identifier ], "{", { match_case }, "}" ; 
    def _parse_type_match(self):
        position = self.current_token.position
        if not self._try_consume(TokenType.MATCH):
            return None
        if not (expression := self._parse_or_expression()):
                raise NoTypeMatchExpressionError(self.current_token)
        identifier = None
        if self._try_consume(TokenType.AS):
            if not (identifier := self._try_consume(TokenType.IDENTIFIER)):
                raise NoIdentifierAfterAs(self.current_token)
            identifier = identifier.value
        self._must_be(TokenType.LBRACE)
        cases = []
        while match_case := self._parse_match_case():
            cases.append(match_case)
        self._must_be(TokenType.RBRACE)
        return TypeMatch(position, expression, cases, identifier)


    # match_case ::= type, "=>", block | "null", "=>", block | "_", "=>", block ;
    def _parse_match_case(self):
        position = self.current_token.position
        if self._try_consume(TokenType.NULL):
            type = VoidType(position, "null")
        elif self._try_consume(TokenType.UNDERSCORE):
            type = AnyType(position, "_")
        else:
            if not (type := self._parse_type()):
                return None
        self._must_be(TokenType.ARROW)
        if not (block := self._parse_block()):
            raise NoBlockInMatchCaseError(position, self.current_token)
        return MatchCase(position, type, block)
            


   # if_statement ::= "if", "(", expression, ")", block, [ "else", block ] ;
    def _parse_if_statement(self):
        if not self._try_consume(TokenType.IF):
            return None
        position = self.current_token.position
        self._must_be(TokenType.LPAREN)
        if not (condition := self._parse_or_expression()):
            raise NoIfCondition(self.current_token)
        self._must_be(TokenType.RPAREN)
        if not (if_block := self._parse_block()):
            ExpectedIfBlockOfStatements(self.current_token)
        else_block = None
        if self._try_consume(TokenType.ELSE):
            if not (else_block := self._parse_block()):
                raise ExpectedElseBlockOfStatements(self.current_token)
        return IfStatement(position, condition, if_block, else_block)
    
    #while_loop ::= "while", "(", expression, ")", block ;
    def _parse_while_loop(self):
        if self._try_consume(TokenType.WHILE):
            position = self.current_token.position
            self._must_be(TokenType.LPAREN)
            if not (while_condition := self._parse_or_expression()):
                raise InvalidWhileCondition(self.current_token)
            self._must_be(TokenType.RPAREN)
            if not (while_block := self._parse_block()):
                raise ExpectedWhileBlockOfStatements(self.current_token)
            return WhileStatement(position, while_condition, while_block)
        return None
    
    def _parse_break_statement(self):
        position = self.current_token.position
        if not self._try_consume(TokenType.BREAK):
            return None
        self._must_be(TokenType.SEMICOLON)
        return BreakStatement(position)
    
    # for_each_loop ::= "for", "each", "(", identifier, ",", identifier, ")", "in", expression, block ;
    def _parse_for_each_loop(self):
        position = self.current_token.position
        if self._try_consume(TokenType.FOR):
            self._must_be(TokenType.EACH)
            self._must_be(TokenType.LPAREN)
            key = self._must_be(TokenType.IDENTIFIER).value
            self._must_be(TokenType.COMMA)
            value = self._must_be(TokenType.IDENTIFIER).value
            self._must_be(TokenType.RPAREN)
            self._must_be(TokenType.IN)
            if not (expr := self._parse_or_expression()):
                raise NoForEachExpression(self.current_token)
            if not (for_each_block := self._parse_block()):
                raise ExpectedForEachBlockOfStatements(self.current_token)
            return ForEachStatement(position, key, value, expr, for_each_block)
        return None
    
    # return_statement ::= "return", [ expression ], ";" ;
    def _parse_return_statement(self):
        position = self.current_token.position
        if not self._try_consume(TokenType.RETURN):
            return None
        expr = self._parse_or_expression()
        self._must_be(TokenType.SEMICOLON)
        return ReturnStatement(position, expr)
    
    # obj_access ::= identifier_or_function_call, { ".", identifier_or_function_call } ;
    def _parse_object_access(self):
        position = self.current_token.position
        if (item := self._parse_identifier_or_function_call()) == None:
            return None
        items = [item]
        while self._try_consume(TokenType.DOT):
            item = self._parse_identifier_or_function_call()
            if item is None:
                raise NoFunctionCallInObjectAccess(self.current_token)
            items.append(item)
        if len(items) > 1:
            return ObjectAccess(position, items)
        return items[0]

    # identifier_or_function_call ::= identifier, [ "(", [ arguments ], ")" ] ; 
    def _parse_identifier_or_function_call(self):
        position = self.current_token.position
        if (identifier := self._try_consume(TokenType.IDENTIFIER)) == None:
            return None
        if not self._try_consume(TokenType.LPAREN):
            return Identifier(identifier.position, identifier.value)
        else:
            arguments = self._parse_arguments()
            self._must_be(TokenType.RPAREN)
            return FunctionCall(position, identifier.value, arguments)
    
    # arguments ::= expression, { ",", expression } ;
    def _parse_arguments(self):
        argumentsList = []
        if (argument := self._parse_or_expression()) == None:
            return argumentsList
        argumentsList.append(argument)
        while self._try_consume(TokenType.COMMA):
            if not (argument := self._parse_or_expression()):
                raise NoArgumentExpression(self.current_token)
            argumentsList.append(argument)
        return argumentsList

    # or_expression ::= and_expression, { "||", and_expression } ;
    def _parse_or_expression(self):
        position = self.current_token.position
        if not (left := self._parse_and_expression()):
            return None
        expressions = [left]
        while self._try_consume(TokenType.LOGICAL_OR):
            if not (right := self._parse_and_expression()):
                raise InvalidOrExpression(self.current_token)
            expressions.append(right)
        if len(expressions) == 1:
            return left
        return OrExpression(position, expressions)

     
    # and_expression ::= equality_expression, { "&&", equality_expression } ;
    def _parse_and_expression(self):
        position = self.current_token.position
        if not (left := self._parse_equality_expression()):
            return None
        expressions = [left]
        while self._try_consume(TokenType.LOGICAL_AND):
            if not (right := self._parse_equality_expression()):
                raise InvalidAndExpression(self.current_token)
            expressions.append(right)
        if len(expressions) == 1:
            return left
        return AndExpression(position, expressions)
    
    # equality_expression ::= relational_expression, [ "==" | "!=", relational_expression ] ;
    def _parse_equality_expression(self):
        position = self.current_token.position
        if not (rel_expr := self._parse_relational_expression()):
            return None
        if expression_type := self.LOGIC_OPERATIONS_MAPPING.get(self.current_token.type):
            self._consume_token()
            if not (second_rel_expr := self._parse_relational_expression()):
                raise InvalidEqualityExpression(self.current_token)
            return expression_type(position, rel_expr, second_rel_expr)
        return rel_expr
       
    # relational_expression ::= add_expression, [ "<" | ">" | "<=" | ">=", add_expression ] ;
    def _parse_relational_expression(self):
        position = self.current_token.position
        if not (left := self._parse_add_expression()):
            return None
        if creator := self.LOGIC_OPERATIONS_MAPPING.get(self.current_token.type):
            self._consume_token()
            if not (right := self._parse_add_expression()):
                raise InvalidRelationalExpression(self.current_token)
            return creator(position, left, right)
        return left
    
    
    # add_expression ::= mul_expression, { "+" | "-", mul_expression } ;
    def _parse_add_expression(self):
        position = self.current_token.position
        if not (left := self._parse_multiplication_expression()):
            return None
        while creator := self.ADDITIVE_OPERATORS.get(self.current_token.type):
            self._consume_token()
            if not (right := self._parse_multiplication_expression()):
                raise InvalidAddExpression(self.current_token)
            left = creator(position, left, right)                   
        return left
    

    # mul_expression ::= unary_expression, { "*" | "/", unary_expression } ;
    def _parse_multiplication_expression(self):
        position = self.current_token.position
        if not (left := self._parse_unary_expression()):
            return None
        while creator := self.MUL_OPERATORS.get(self.current_token.type):
            self._consume_token()
            if not (right := self._parse_unary_expression()):
                raise InvalidMultiplicationExpression(self.current_token)
            left = creator(position, left, right)                   
        return left

    
    # unary_expression ::= [ "-" | "not" | "!" ], type_expression ;
    def _parse_unary_expression(self):
        position = self.current_token.position
        negate = False
        if self.current_token.value in ["-", "not", "!"]:
            negate = True
            if self.current_token.value == "-":
                negation_type = "arithmetic"
            else:
                negation_type = "logic"
            self._consume_token()
        if not (type_expr := self._parse_type_expression()):
            return None
        if negate:
            return Negation(position, type_expr, negation_type)
        return type_expr


    # type_expression ::= factor, [ "is", type ] ;
    def _parse_type_expression(self):
        position = self.current_token.position
        if not (factor := self._parse_factor()):
            return None
        if self._try_consume(TokenType.IS):
            if not (type := self._parse_type()):
                raise InvalidTypeExpression(self.current_token)   
            return TypeExpression(position, factor, type)
        return factor
        
    
    # factor ::= literal | "(", expression, ")", | obj_access ;
    def _parse_factor(self):
        factor_value = \
            self._parse_object_access() \
            or self._parse_parenthesized_expression() \
            or self._parse_literal() 
        if factor_value:
            return factor_value
        return None

    def _parse_parenthesized_expression(self):
        if self._try_consume(TokenType.LPAREN):
            if not (expression := self._parse_or_expression()):
                raise InvalidExpression(self.current_token)
            self._must_be(TokenType.RPAREN)
            return expression
        return None


    # literal ::= integer | float | bool | string | dictionary;
    def _parse_literal(self): 
        variable_value = \
            self._parse_bool()    \
            or self._parse_integer()  \
            or self._parse_float()   \
            or self._parse_string()  \
            or self._parse_dictionary() \
            or self._parse_null()
        if variable_value:
            return variable_value
        return None
    
    def _parse_bool(self):
        position = self.current_token.position
        if (token := self._try_consume(self.BOOL)) == None:
            return None
        if token.type == TokenType.TRUE:
            return BoolValue(position, True)
        return BoolValue(position, False)

    def _parse_integer(self):
        position = self.current_token.position
        if (token := self._try_consume(TokenType.INTEGER_VALUE)) == None:
            return None
        return IntegerValue(position, token.value)

    def _parse_float(self):
        position = self.current_token.position
        if (token := self._try_consume(TokenType.FLOAT_VALUE)) == None:
            return None
        return FloatValue(position, token.value)

    def _parse_string(self):
        position = self.current_token.position
        if (token := self._try_consume(TokenType.STRING_VALUE)) == None:
            return None
        return StringValue(position, token.value)
    
    def _parse_null(self):
        position = self.current_token.position
        if (token := self._try_consume(TokenType.NULL)) == None:
            return None
        # return NullValue(position, token.value)
        return NullValue(position, None)
    

    # dictionary ::= "{", [ dict_entries ], "}" ;
    def _parse_dictionary(self):
        position = self.current_token.position
        if self._try_consume(TokenType.LBRACE) == None:
            return None
        if not (dictionary_entries := self._parse_dictionary_entries()):
                raise DictionaryEntriesError(self.current_token) 
        self._must_be(TokenType.RBRACE)
        return Dictionary(position, dictionary_entries)


    # dict_entries ::= expression, ":", expression, { ",", expression, ":", expression } ;
    def _parse_dictionary_entries(self):
        position = self.current_token.position
        if not (entry := self._parse_dictionary_entry()):
            return None
        entries = [entry]
        while self._try_consume(TokenType.COMMA):
            if not (entry := self._parse_dictionary_entry()):
                raise DictionaryEntriesError(self.current_token) 
            entries.append(entry)
        return entries
            
    
    def _parse_dictionary_entry(self):
        position = self.current_token.position
        if not (expression := self._parse_or_expression()):
            return None
        self._must_be(TokenType.COLON)
        if not (expression2 := self._parse_or_expression()):
            raise DictionaryEntryError(self.current_token)
        return  DictionaryEntry(position, expression, expression2)


    # parameters ::= parameter, { ",", parameter } ;
    def _parse_parameters(self):
        params = []
        if (param := self._parse_parameter()) is None:
            return params
        params.append(param)
        while self._try_consume(TokenType.COMMA):
            if not (param := self._parse_parameter()):
                raise InvalidParameterError(self.current_token)
            elif any(existing_param.name == param.name for existing_param in params):
                raise SameParameterError(self.current_token)
            else:
                params.append(param)
        return params


# parameter ::= type_or_variant, identifier ;
    def _parse_parameter(self):
        position = self.current_token.position
        if (token_type := self._parse_type()) == None:
            return None
        if param := self._try_consume(TokenType.IDENTIFIER):
            return Parameter(position, token_type, param.value)
        raise NoIdentifierInDeclaration(self.current_token)
    

    # func_type ::= type | "void";
    def _parse_func_type(self):
        token = self.current_token
        if (type := self.TYPE_MAPPING.get(self.current_token.type)):
            pass
        elif token.type == TokenType.VOID:
            type = VoidType
        else:
            return None
        self._consume_token()
        return type(token.position, token.value)


    def _parse_type(self):
        token = self.current_token
        if (type := self.TYPE_MAPPING.get(self.current_token.type)):
            self._consume_token()
            return type(token.position, token.value)
        else:
            return None
    