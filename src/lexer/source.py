import io

class Source():
    def __init__(self, text):
        self.text = text
        self.column = 1
        self.line = 1
        self.current_char = self.text.read(1)
        # self.get_next_char()
    
    def get_current_char(self) -> str:
        return self.current_char

    def get_next_char(self) -> str:
        self.current_char = self.text.read(1)
        if self.current_char != '':
            self.column += 1
        if self.current_char in ('\r', '\n'):
            self.line += 1
            self.column = 1
        return self.get_current_char()

    # def get_next_char(self) -> str:
    #     if self.current_char == '':  # sprawdzenie czy już nie jesteśmy na EOF
    #         return self.current_char
        
    #     self.current_char = self.text.read(1)
        
    #     if self.current_char == '\n':
    #         self.line += 1
    #         self.column = 0
    #     elif self.current_char == '\r':
    #         # Sprawdzanie, czy kolejny znak to '\n'
    #         next_char = self.text.read(1)
    #         if next_char != '\n':
    #             self.text.seek(-1, io.SEEK_CUR)  # cofnij o jeden znak, jeśli to nie '\n'
    #         self.line += 1
    #         self.column = 0
    #     elif self.current_char != '':
    #         self.column += 1
        
    
    def get_current_position(self) -> tuple:
        return (self.column, self.line)
    
    def set_start_position(self) -> None:
        self.column = 0
        self.line = 1
        self.text.seek(0)
        self.get_next_char()

    def get_line(self, line_number: int) -> str:
        self.text.seek(0)
        for i in range(line_number):
            line = self.text.readline()
        return line
    
    def peek_next_char(self) -> str:
        current_position = self.text.tell() 
        next_char = self.text.read(1) 
        self.text.seek(current_position) 
        return next_char

    def __str__(self) -> str:
        return self.text.getvalue()
    

    
class String(Source):
    def __init__(self, text):
        super().__init__(io.StringIO(text))

class File(Source):
    def __init__(self, path):
        self.file = open(path, 'r')
        super().__init__(self.file)

s = String("\r\na\rb")
s.get_next_char()
s.get_next_char()
s.get_next_char()
s.get_next_char()
print(s.get_current_char())
print(s.get_current_position())

    # source = String("\r\na\rb")
    # assert source.get_current_char() == "\n"
    # assert source.get_current_position() == (1, 1)
    # assert source.get_current_char() == "a"
    # assert source.get_current_position() == (1, 2)
    # assert source.get_next_char() == "\r"
    # assert source.get_current_position() == (2, 2)
    # assert source.get_current_char() == "b"
    # assert source.get_current_position() == (3, 2)