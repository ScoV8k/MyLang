from enum import Enum, auto

class TokenType(Enum):
    # keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    EACH = auto()
    IN = auto()
    RETURN = auto()
    MATCH = auto()
    AS = auto()
    TRUE = auto()
    FALSE = auto()
    VOID = auto()
    IS = auto()
    NULL = auto()
    BREAK = auto()
    
    # types
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    DICT = auto()
    VARIANT = auto()
    
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
    ARROW = auto() 
    COMMENT = auto()

    # chars
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    UNDERSCORE = auto()

    # diff
    IDENTIFIER = auto()
    INTEGER_VALUE = auto()
    FLOAT_VALUE = auto()
    STRING_VALUE = auto()
    UNKNOWN = auto()
    EOF = auto()

class Symbols:
    keywords = {
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "for": TokenType.FOR,
        "each": TokenType.EACH,
        "in": TokenType.IN,
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
        "variant": TokenType.VARIANT,
        "is": TokenType.IS,
        "null": TokenType.NULL,
        "dict": TokenType.DICT,
        "break": TokenType.BREAK 
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
        ':': TokenType.COLON,
        '<': TokenType.LESS_THAN,
        '>': TokenType.GREATER_THAN,
        '!': TokenType.NOT,
        '#': TokenType.COMMENT,
        '_': TokenType.UNDERSCORE
    }

    double_chars = {
        '==': TokenType.EQUALS,
        '!=': TokenType.NOT_EQUALS,
        '<=': TokenType.LESS_THAN_EQUAL,
        '>=': TokenType.GREATER_THAN_EQUAL,
        '&&': TokenType.LOGICAL_AND,
        '||': TokenType.LOGICAL_OR,
        '=>': TokenType.ARROW,
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

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and 
                self.value == other.value and 
                self.position == other.position)