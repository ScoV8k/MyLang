from src.lexer.tokens import TokenType, Symbols, Token
# from src.lexer.source import Source, String, File
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError, LeadingZeroError, IdentifierTooLongError, NumberTooBigError, StringTooLongError, UnterminatedStringError, InvalidEscapeSequenceError, CommentTooLongError, TooManyWhitespacesError, UnknownTokenError
import io
# from tokens import TokenType, Symbols, Token
# from source import Source, String, File

MAX_IDENTIFIER_LENGTH = 128
MAX_INT = 2147483647
MAX_FLOAT = 3.402823466e+38
MAX_STRING_LENGTH = 2**16
MAX_COMMENT_LENGTH = 256
MAX_WHITESPACES = 1024


class Lexer():
    def __init__(self, source, error_manager) -> None: 
        # MAX_IDENTIFIER_LENGTH = 128
        # MAX_INT = 2147483647
        # MAX_FLOAT = 3.402823466e+38
        # MAX_STRING_LENGTH = 2**16
        # MAX_COMMENT_LENGTH = 256
        # MAX_WHITESPACES = 1024
        self.source = source
        self.current_char = chr(2)
        self.etx = chr(3)
        self.column = 0
        self.line = 1
        self.last_char_part_of_newline = False
        self.error_manager = error_manager
        self._get_next_char()

    def _get_next_char(self):
        if self.current_char == self.etx:
            return self.current_char
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.current_char = self.source.read(1)
        if self.current_char == '':
            self.current_char = self.etx
        self.column += 1
        self._check_newline()
        return self.current_char
    
    
    def _check_newline(self):
        next_char = self._peek_next_char()
        potential_double_char = self.current_char + next_char
        if potential_double_char in ['\n\r', '\r\n']:
            self.current_char = '\n'
            self.source.read(1)
        elif self.current_char == '\r':
            self.current_char = '\n'


    def _get_current_position(self) -> tuple:
        return (self.line, self.column)
    
    def _peek_next_char(self) -> str:
        curr_pos = self.source.tell()
        next_char = self.source.read(1) 
        self.source.seek(curr_pos) 
        return next_char
    
    def _try_build_identifier_or_keyword(self) -> Token: 
        if self.current_char.isalpha():
            position = self._get_current_position()
            value = [self.current_char]
            self._get_next_char()
            while self.current_char.isalnum() or self.current_char == '_':
                if len(value) >= MAX_IDENTIFIER_LENGTH:
                    value = "".join(value)
                    self.error_manager.add_error(IdentifierTooLongError(position, value))
                    raise IdentifierTooLongError(position, value)
                value.append(self.current_char)
                self._get_next_char()
            value = "".join(value)
            return Token(Symbols.keywords.get(value, TokenType.IDENTIFIER), value, position)
    


    def _try_build_number(self) -> Token: 
        if not self.current_char.isdecimal():
            return None
        position = self._get_current_position()

        if self.current_char == '0' and self._peek_next_char().isdecimal():
            self.error_manager.add_error(LeadingZeroError(position))
            while self.current_char.isdecimal() or self.current_char == ".":
                self._get_next_char()
            return Token(TokenType.INTEGER_VALUE, None, position)
    
        value = int(self.current_char)
        self._get_next_char()
        while self.current_char.isdecimal():
            if value > (MAX_INT - int(self.current_char)) / 10:
                self.error_manager.add_error(NumberTooBigError(position, value))
                raise NumberTooBigError(position, value)
            value = value * 10 + int(self.current_char) # <= MAX_INT
            self._get_next_char()
        if self.current_char == '.':
            self._get_next_char()
            decimals = int(self.current_char)
            decimal_place = 1
            self._get_next_char()

            while self.current_char.isdecimal():
                decimals = decimals * 10 + int(self.current_char)
                self._get_next_char()
                decimal_place += 1
            float_value = float(value + decimals / 10**decimal_place)
            if abs(float_value) > MAX_FLOAT:
                self.error_manager.add_error(NumberTooBigError(position, float_value))
                float_value = None
            return Token(TokenType.FLOAT_VALUE, float_value , position)
        return Token(TokenType.INTEGER_VALUE, value, position)

    def _try_build_string(self) -> Token: 
        if self.current_char == '"':
            position = self._get_current_position()
            value = []
            self._get_next_char()
            while self.current_char != '"' and self.current_char != self.etx:
                char = self._handle_escaping(value)
                if len(value) >= MAX_STRING_LENGTH:
                    self.error_manager.add_error(StringTooLongError(position))
                    raise StringTooLongError(position)
                value.append(char)
                self._get_next_char()
            if self.current_char == self.etx:
                self.error_manager.add_error(UnterminatedStringError(position))
            self._get_next_char()
            value = "".join(value)
            return Token(TokenType.STRING_VALUE, value, position) 

    def _handle_escaping(self, value):
        if self.current_char == '\\':
            self._get_next_char()
            match self.current_char:
                case 'n':
                    char = '\n'
                case 't':
                    char = '\t'
                case '\\':
                    char = '\\'
                case '"':
                    char = '\"'
                case  "'":
                    char = "\'"
                case _:
                    self.error_manager.add_error(InvalidEscapeSequenceError(self._get_current_position(), self.current_char))
                    char = self.current_char
        else:
            char = self.current_char
        return char

    def _try_build_symbol(self) -> Token:   
        current_char = self.current_char
        position = self._get_current_position()
        next_char = self._peek_next_char()
        potential_double_char = current_char + next_char
        if token_type:= Symbols.double_chars.get(potential_double_char):
            self._get_next_char() 
            self._get_next_char()
            return Token(token_type, potential_double_char, position)
        elif token_type:= Symbols.chars.get(current_char):
            if next_char and current_char in ['&', '|']:
                self.error_manager.add_error(InvalidTokenError(position, current_char))
            value = current_char
            self._get_next_char()
            return Token(token_type, value, position)

    def _try_build_comment(self) -> Token:
        if self.current_char == '#':
            position = self._get_current_position()
            value = [self.current_char]
            self._get_next_char()
            while self.current_char not in ('\r', '\n') and self.current_char != self.etx:
                if len(value) >= MAX_COMMENT_LENGTH:
                    self.error_manager.add_error(CommentTooLongError(position))
                    raise CommentTooLongError(position)
                value.append(self.current_char)
                self._get_next_char()
            value = "".join(value)
            return Token(TokenType.COMMENT, value, position)
    
    def _try_build_eof(self) -> Token:
        if self.current_char == self.etx:
            return Token(TokenType.EOF, None, self._get_current_position())
    
    def _skip_whitespaces(self):
        position = self._get_current_position()
        whitespace_count = 0
        while self.current_char.isspace():
            whitespace_count += 1
            if whitespace_count > MAX_WHITESPACES:
                self.error_manager.add_error(TooManyWhitespacesError(position))
                raise TooManyWhitespacesError(position)
            self._get_next_char()

    def get_next_token(self) -> Token:
        self._skip_whitespaces()
        for fun in [self._try_build_identifier_or_keyword,
                    self._try_build_number,
                    self._try_build_string,
                    self._try_build_comment,
                    self._try_build_symbol,
                    self._try_build_eof,
                    ]:
            if token := fun():
                return token
        self.error_manager.add_error(UnknownTokenError(self._get_current_position(), self.current_char))
        token = Token(TokenType.UNKNOWN, None, self._get_current_position())
        self._get_next_char()
        return token
            
    def __iter__(self): 
        token = self.get_next_token()
        while token.type != TokenType.EOF:
            yield token
            token = self.get_next_token()
        yield token