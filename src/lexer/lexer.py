from src.lexer.tokens import TokenType, Symbols, Token
from src.lexer.source import Source, String, File
# from errors.error_manager import ErrorManager
# from errors import InvalidTokenError
import io
# from tokens import TokenType, Symbols, Token
# from source import Source, String, File

class Lexer():
    def __init__(self, source) -> None:
        self.source = source
        self.current_char = None
        self.column = 0
        self.line = 1
        self.newline = None
        self.last_char_part_of_newline = False
        # self.error_manager = ErrorManager()
        self.buffered_newline = False 
        self.last_cr = False
        self._get_next_char()


    def _get_current_char(self) -> str:
        return self.current_char
    
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
        if self.newline:
            self.line += 1
            self.column = 0
            self.newline = None
        self.current_char = self.source.read(1)
        if self.current_char:
            self.column += 1
        self.check_newline()
        return self.current_char
    
    def check_newline(self):
        next_char = self._peek_next_char()
        potential_double_char = self.current_char + next_char
        if potential_double_char in ['\n\r', '\r\n']:
            self.current_char = '\n'
            self.source.read(1)
            self.newline = True
        elif self.current_char in ['\n', '\r']:
            self.newline = True


    def _get_current_position(self) -> tuple:
        return (self.column, self.line)
    
    def _peek_next_char(self) -> str:
        # return self.source.peek_next_char()
        curr_pos = self.source.tell()
        next_char = self.source.read(1) 
        self.source.seek(curr_pos) 
        return next_char
    
    def try_build_identifier_or_keyword(self) -> Token:
        if self._get_current_char().isalpha():
            position = self._get_current_position()
            value = [self._get_current_char()]
            self._get_next_char()
            while self._get_current_char().isalnum() or self._get_current_char() == '_':
                value.append(self._get_current_char()) # do zmainy obsluzyć max dlugosc
                self._get_next_char()
            value = "".join(value)
            return Token(Symbols.keywords.get(value, TokenType.IDENTIFIER), value, position)
    
    # def try_build_number(self) -> Token: # budujemy liczbe 1 (123)
    #     if self._get_current_char().isdecimal():
    #         position = self._get_current_position()
    #         value = self._get_current_char()
    #         self._get_next_char()
    #         while self._get_current_char().isdecimal(): # 007 jest ok, dodać zakresy wartości dla liczb
    #             value += self._get_current_char()
    #             self._get_next_char()
    #         if self._get_current_char() == '.':
    #             value += self._get_current_char()
    #             self._get_next_char()
    #             while self._get_current_char().isdecimal():
    #                 value += self._get_current_char()
    #                 self._get_next_char()
    #             return Token(TokenType.FLOAT_VALUE, value, position)
    #         return Token(TokenType.INTEGER_VALUE, value, position)


    def try_build_number(self) -> Token: # budujemy liczbe 1 (123)
        if self._get_current_char().isdecimal():
            position = self._get_current_position()
            value = int(self._get_current_char())
            self._get_next_char()
            while self._get_current_char().isdecimal(): # 007 jest ok, dodać zakresy wartości dla liczb
                value = value * 10 + int(self._get_current_char())
                self._get_next_char()
            if self._get_current_char() == '.':
                self._get_next_char()
                decimals = int(self._get_current_char())
                decimal_place = 1
                self._get_next_char()

                while self._get_current_char().isdecimal():
                    decimals = decimals * 10 + int(self._get_current_char())
                    self._get_next_char()
                    decimal_place += 1
                return Token(TokenType.FLOAT_VALUE, float(value + decimals / 10**decimal_place) , position)
            return Token(TokenType.INTEGER_VALUE, value, position)

    def try_build_string(self) -> Token: # budujemy string na liście, max dlugosc stringa, weryfikacja czy string nie jest przelamany znakiem nowej lini, obsluzyć nie zamkniety string "asd
        if self._get_current_char() == '"':
            position = self._get_current_position()
            value = []
            self._get_next_char()
            while self._get_current_char() != '"':
                if self._get_current_char() == '\\':
                    self._get_next_char()
                    if self._get_current_char() == 'n':
                        char = '\n'
                    elif self._get_current_char() == 't':
                        char = '\t'
                    elif self._get_current_char() == '\\':
                        char = '\\'
                    elif self._get_current_char() == '"':
                        char = '\"'
                    elif self._get_current_char() == "'":
                        char = "\'"
                else:
                    char = self._get_current_char()
                value.append(char)
                self._get_next_char()
            self._get_next_char()
            value = "".join(value)
            return Token(TokenType.STRING_VALUE, value, position) 

    def try_build_symbol(self) -> Token:    # obslużyć jednego &, komunikuje bład ale zwraca && i ||
        current_char = self._get_current_char()
        position = self._get_current_position()
        next_char = self._peek_next_char()
        potential_double_char = current_char + next_char
        if potential_double_char in Symbols.double_chars:
            self._get_next_char() 
            self._get_next_char()
            value = potential_double_char
            return Token(Symbols.double_chars[value], value, position)
        elif current_char in Symbols.chars:
            if next_char and current_char + next_char not in Symbols.double_chars and current_char in ['&', '|']:
                self.error_manager.add_error(InvalidTokenError(position, current_char))
            value = current_char
            self._get_next_char()
            return Token(Symbols.chars[value], value, position)

    def try_build_comment(self) -> Token: # ograniczenie długości komentarza
        if self._get_current_char() == '#':
            position = self._get_current_position()
            value = [self._get_current_char()]
            self._get_next_char()
            while self._get_current_char() not in ('\r', '\n') and self._get_current_char() != '':
                value.append(self._get_current_char()) # nie budujemy stringa
                self._get_next_char()
            value = "".join(value)
            return Token(TokenType.COMMENT, value, position)
    
    def try_build_eof(self) -> Token:
        if self._get_current_char() == '':
            pos = self._get_current_position()
            return Token(TokenType.EOF, None, pos)
    
    def skip_whitespaces(self): # ogranicznik
        while self._get_current_char().isspace():
            self._get_next_char()

    def get_next_token(self) -> Token:
        self.skip_whitespaces()
        for fun in [self.try_build_identifier_or_keyword,
                    self.try_build_number,
                    self.try_build_string,
                    self.try_build_comment,
                    self.try_build_symbol,
                    self.try_build_eof,
                    ]:
            if token := fun():
                return token
        raise InvalidTokenError(self._get_current_position(), self._get_current_char())
            
    def get_all_tokens(self):
        tokens = []
        token = self.get_next_token()
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        return tokens
    
    
s = String("\r\na\rb")
# l = Lexer(io.StringIO("\r\na\rb"))
l = Lexer(io.StringIO("a\nb\n"))
print(l._get_current_char())
print(l._get_current_position())
print(l._get_next_char())
print(l._get_current_position())
print(l._get_next_char())
print(l._get_current_position())
print(l._get_next_char())
print(l._get_current_position())

# print(l.get_next_token())
# print(l.get_next_token())



    # source = String("\r\na\rb")
    # assert source.get_current_char() == "\n"
    # assert source.get_current_position() == (1, 1)
    # assert source.get_current_char() == "a"
    # assert source.get_current_position() == (1, 2)
    # assert source.get_next_char() == "\r"
    # assert source.get_current_position() == (2, 2)
    # assert source.get_current_char() == "b"
    # assert source.get_current_position() == (3, 2)