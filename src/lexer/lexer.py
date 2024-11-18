from src.lexer.tokens import TokenType, Symbols, Token
# from src.lexer.source import Source, String, File
from src.errors.error_manager import ErrorManager
from src.errors.lexer_errors import InvalidTokenError
import io
# from tokens import TokenType, Symbols, Token
# from source import Source, String, File


class Lexer():
    def __init__(self, source) -> None: # error manager dostarczany z zewnatrz
        self.source = source
        self.current_char = chr(2)
        self.column = 0
        self.line = 1
        self.last_char_part_of_newline = False
        self.error_manager = ErrorManager()
        self._get_next_char()


    # def _get_current_char(self) -> str: # do wywalenia
    #     return self.current_char
    
    # def _get_next_char(self) -> str:
    #     return self.source.get_next_char()


    # def _get_next_char(self):
    #     # Read the next character from the source
    #     self.current_char = self.source.read(1)

    #     # Check if the previous character was a newline character
    #     if self.current_char == '\n':
    #         self.line += 1
    #         self.column = 1
    #     elif self.current_char == '\r':  # Handle '\r' specifically
    #         # Peek next char to check if it's '\n'
    #         next_char = self.source.read(1)
    #         if next_char == '\n':
    #             self.current_char = '\n'  # Treat '\r\n' as '\n'
    #         else:
    #             self.source.seek(self.source.tell() - 1)  # Unread the peeked char
    #         self.line += 1
    #         self.column = 1
    #     else:
    #         self.column += 1

    #     return self.current_char

    def _get_next_char(self):
        if self.current_char == '':
            return self.current_char
        if self.current_char == '\n':   #self.newline: 
            self.line += 1
            self.column = 0
        self.current_char = self.source.read(1)
        # if self.current_char:
        self.column += 1
        self.check_newline()
        return self.current_char
    
    def check_newline(self):
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
        # return self.source.peek_next_char()
        curr_pos = self.source.tell()
        next_char = self.source.read(1) 
        self.source.seek(curr_pos) 
        return next_char
    
    def _try_build_identifier_or_keyword(self) -> Token: # ograniczenie na długość
        if self.current_char.isalpha():
            position = self._get_current_position()
            value = [self.current_char]
            self._get_next_char()
            while self.current_char.isalnum() or self.current_char == '_':
                value.append(self.current_char)
                self._get_next_char()
            value = "".join(value)
            return Token(Symbols.keywords.get(value, TokenType.IDENTIFIER), value, position)
    


    def _try_build_number(self) -> Token: # dodać ogranicznik, nie pozwalać na 007
        if self.current_char.isdecimal():
            position = self._get_current_position()
            value = int(self.current_char)
            self._get_next_char()
            while self.current_char.isdecimal(): 
                value = value * 10 + int(self.current_char)
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
                if self.current_char == '.':
                    self.error_manager.add_error(InvalidTokenError(self._get_current_position(), self.current_char))
                return Token(TokenType.FLOAT_VALUE, float(value + decimals / 10**decimal_place) , position)
            return Token(TokenType.INTEGER_VALUE, value, position)

    def _try_build_string(self) -> Token: # dlugosc stringa max
        if self.current_char == '"':
            position = self._get_current_position()
            value = []
            self._get_next_char()
            while self.current_char != '"' and self.current_char != '':
                char = self._handle_escaping(value)
                value.append(char)
                self._get_next_char()
            if self.current_char == '':
                self.error_manager.add_error(InvalidTokenError(self._get_current_position(), self.current_char)) # Zmienic blad na
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
                    self.error_manager.add_error(InvalidTokenError(self._get_current_position(), self.current_char)) # inny blad
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

    def _try_build_comment(self) -> Token: # ograniczenie długości komentarza
        if self.current_char == '#':
            position = self._get_current_position()
            value = [self.current_char]
            self._get_next_char()
            while self.current_char not in ('\r', '\n') and self.current_char != '':
                value.append(self.current_char)
                self._get_next_char()
            value = "".join(value)
            return Token(TokenType.COMMENT, value, position)
    
    def _try_build_eof(self) -> Token:
        if self.current_char == '':
            return Token(TokenType.EOF, None, self._get_current_position())
    
    def _skip_whitespaces(self): # ogranicznik
        while self.current_char.isspace():
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
        # raise InvalidTokenError(self._get_current_position(), self.current_char)
        self.error_manager.add_error(InvalidTokenError(self._get_current_position(), self.current_char))
        token = Token(TokenType.UNKNOWN, None, self._get_current_position())
        self._get_next_char()
        return token
            
    def get_all_tokens(self):
        tokens = []
        token = self.get_next_token()
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        return tokens
    