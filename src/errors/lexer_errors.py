# class InvalidTokenError(Excetion):
#     def __init__(self, position, char):
#         line, column = position
#         text = f"LexicalError ({line}, {column}): Niezgodny znak: \'{char}\'."
#         self.message = text
#         super().__init__(self.message)

#     def __str__(self):
#         return self.message
    

class LexerError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
    

class InvalidTokenError(LexerError):
    def __init__(self, position, char):
        line, column = position
        message = f"LexicalError ({line}, {column}): Niezgodny znak: \'{char}\'."
        super().__init__(message)