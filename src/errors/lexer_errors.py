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
    
    def __eq__(self, other):
        if not isinstance(other, LexerError):
            return False
        return self.message == other.message


class InvalidTokenError(LexerError):
    def __init__(self, position, char):
        line, column = position
        message = f"InvalidTokenError ({line}, {column}): Niezgodny znak: '{char}'."
        super().__init__(message)

class UnknownTokenError(LexerError):
    def __init__(self, position, char):
        line, column = position
        message = f"UnknownTokenError ({line}, {column}): Niezgodny token: '{char}'."
        super().__init__(message)


class IdentifierTooLongError(LexerError):
    def __init__(self, position, identifier):
        line, column = position
        message = f"IdentifierTooLongError ({line}, {column}): Identyfikator '{identifier}' jest zbyt długi."
        super().__init__(message)


class NumberTooBigError(LexerError):
    def __init__(self, position, number):
        line, column = position
        message = f"NumberTooBigError ({line}, {column}): Liczba '{number}' przekracza dozwoloną wielkość."
        super().__init__(message)


class LeadingZeroError(LexerError):
    def __init__(self, position):
        line, column = position
        message = f"LeadingZeroError ({line}, {column}): Liczby nie mogą zawierać zer wiodących (np. '007')."
        super().__init__(message)


class StringTooLongError(LexerError):
    def __init__(self, position):
        line, column = position
        message = f"StringTooLongError ({line}, {column}): String przekracza maksymalną dozwoloną długość."
        super().__init__(message)


class UnterminatedStringError(LexerError):
    def __init__(self, position):
        line, column = position
        message = f"UnterminatedStringError ({line}, {column}): String nie został poprawnie zakończony."
        super().__init__(message)


class CommentTooLongError(LexerError):
    def __init__(self, position):
        line, column = position
        message = f"CommentTooLongError ({line}, {column}): Komentarz przekracza maksymalną dozwoloną długość."
        super().__init__(message)

class InvalidEscapeSequenceError(LexerError):
    def __init__(self, position, sequence):
        line, column = position
        message = f"InvalidEscapeSequenceError ({line}, {column}): Niepoprawna sekwencja ucieczki '\\{sequence}'."
        super().__init__(message)

class TooManyWhitespacesError(LexerError):
    def __init__(self, position):
        line, column = position
        message = f"TooManyWhitespacesError ({line}, {column}): Zbyt wiele spacji w jednym ciągu."
        super().__init__(message)

