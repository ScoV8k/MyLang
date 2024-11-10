from enum import Enum, auto

class TokenType(Enum):
    # keywords
    CLASS = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    # FUN = auto()
    MATCH = auto()
    AS = auto()
    TRUE = auto()
    FALSE = auto()
    VOID = auto()
    IS = auto()

    # types
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()

    # operators
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_THAN_EQUAL = auto()
    GREATER_THAN_EQUAL = auto()
    LOGICAL_AND = auto()
    LOGICAL_OR = auto()
    NOT = auto()
    RETURN_SIGN = auto() # zmienic na arrow
    COMMENT = auto()


    # chars
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()

    # diff
    IDENTIFIER = auto()
    INTEGER_VALUE = auto()
    FLOAT_VALUE = auto()
    STRING_VALUE = auto()
    EOF = auto()

class Symbols:

    keywords = {
            "class": TokenType.CLASS,
            # "fun": TokenType.FUN,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "return": TokenType.RETURN,
            "match": TokenType.MATCH,
            "as": TokenType.AS,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "int": TokenType.INT,
            "float": TokenType.FLOAT,
            "bool": TokenType.BOOL,
            "string": TokenType.STRING,
            "void": TokenType.VOID,
            "is": TokenType.IS,
        }

    chars = {
            '=': TokenType.ASSIGN,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '<': TokenType.LESS_THAN,
            '>': TokenType.GREATER_THAN,
            '!': TokenType.NOT,
            '#': TokenType.COMMENT,
        }
    double_chars = {
            '==': TokenType.EQUALS,
            '!=': TokenType.NOT_EQUALS,
            '<=': TokenType.LESS_THAN_EQUAL,
            '>=': TokenType.GREATER_THAN_EQUAL,
            '&&': TokenType.LOGICAL_AND,
            '||': TokenType.LOGICAL_OR,
            '->': TokenType.RETURN_SIGN,
            }
        
class Token:
    def __init__(self, type: TokenType, value, position: tuple) -> None:
        self.type = type
        self.value = value
        self.position = position

    def __str__(self):
        return f'Token({self.type}, {self.value}, {self.position})'
    
    def __repr__(self):
        return f'Token({self.type}, {self.value}, {self.position})'
    