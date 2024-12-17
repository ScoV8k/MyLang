class ParserError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
    
    def __eq__(self, other):
        if not isinstance(other, ParserError):
            return False
        return self.message == other.message


class UnexpectedToken(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"UnexpectedToken ({line}, {column}): Niespodziewany token: '{token.value}'."
        super().__init__(message)


class BuildingFunctionError(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"SyntaxError ({line}, {column}): Błąd podczas budowania definicji funkcji '{token.value}'."
        super().__init__(message)


class InvalidParameterError(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidParameterError ({line}, {column}): Nie podano prawidłowego parametru."
        super().__init__(message)


class SameParameterError(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"SameParameterError ({line}, {column}): Podano 2 takie same parametry '{token.value}'."
        super().__init__(message)


class EmptyBlockOfStatements(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"EmptyBlockOfStatements ({line}, {column}): Podano pusty blok. Wymagany statement: '{token.value}'."
        super().__init__(message)


class InvalidRelationalExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidRelationalExpression ({line}, {column}): Niepoprawne wyrażenie po operatorze relacyjnym: '{token.value}'."
        super().__init__(message)


class InvalidEqualityExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidEqualityExpression ({line}, {column}): Niepoprawne wyrażenie po operatorze porównania: '{token.value}'."
        super().__init__(message)


class NoForEachExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"NoForEachExpression ({line}, {column}): Brak wyrażenia w instrukcji 'for each': '{token.value}'."
        super().__init__(message)

class NoIfCondition(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"NoIfCondition ({line}, {column}): Wymagany warunek struktury if '{token.value}'."
        super().__init__(message)


class ExpectedIfBlockOfStatements(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"ExpectedIfBlockOfStatements ({line}, {column}): Wymagany block po strukturze if '{token.value}'."
        super().__init__(message)

class ExpectedElseBlockOfStatements(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"ExpectedElseBlockOfStatements ({line}, {column}): Wymagany block po strukturze else '{token.value}'."
        super().__init__(message)

        
class InvalidWhileCondition(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidWhileCondition ({line}, {column}): Niepoprawny warunek pętli while '{token.value}'."
        super().__init__(message)

class ExpectedWhileBlockOfStatements(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"ExpectedWhileBlockOfStatement: ({line}, {column}): Wymagany block po strukturze while '{token.value}'."
        super().__init__(message)

class ExpectedForEachBlockOfStatements(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"ExpectedForEachBlockOfStatements: ({line}, {column}): Wymagany block po strukturze for each '{token.value}'."
        super().__init__(message)


class NoArgumentExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"NoArgumentExpression: ({line}, {column}): Brak wyrazenia przy parsowaniu argumentow:  '{token.value}'."
        super().__init__(message)


class InvalidOrExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidOrExpression: ({line}, {column}): Brak wyrazenia po operatorze or: '{token.value}'."
        super().__init__(message)


class InvalidAndExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidAndExpression: ({line}, {column}): Brak wyrazenia po operatorze and: '{token.value}'."
        super().__init__(message)


class InvalidLogicExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidLogicExpression: ({line}, {column}): Niepoprawne wyrazenie po operatorze relacyjnym: '{token.value}'."
        super().__init__(message)


class InvalidExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidExpression: ({line}, {column}): Oczekiwano wyrazenia: '{token.value}'."
        super().__init__(message)


class InvalidArithmeticExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidArithmeticExpression: ({line}, {column}): Niepoprawne wyrazenie po operatorze arytmetycznym: '{token.value}'."
        super().__init__(message)

class InvalidNegationExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidNegationExpression: ({line}, {column}): Niepoprawne wyrazenie po operatorze negacji: '{token.value}'."
        super().__init__(message)


class DictionaryEntriesError(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"DictionaryEntriesError: ({line}, {column}): Wymagane podanie wartosci slownika '{token.value}'."
        super().__init__(message)

class DictionaryEntryError(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"DictionaryEntryError: ({line}, {column}): Niepoprawna wartosc slowika '{token.value}'."
        super().__init__(message)

class NoTypeMatchExpressionError(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"NoTypeMatchExpressionError: ({line}, {column}): Brak wyrażenia w instrukcji 'match': '{token.value}'."
        super().__init__(message)


class NoIdentifierAfterAs(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"NoIdentifierAfterAs: ({line}, {column}): Oczekiwano identyfikatora po słowie kluczowym 'as': '{token.value}'."
        super().__init__(message)


class NoBlockInMatchCaseError(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"NoBlockInMatchCaseError: ({line}, {column}): Oczekiwano bloku kodu w instrukcji 'match': '{token.value}'."
        super().__init__(message)


class InvalidMultiplicationExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidMultiplicationExpression: ({line}, {column}): Niepoprawne wyrażenie po operatorze mnożenia/dzielenia: '{token.value}'."
        super().__init__(message)

class InvalidAddExpression(ParserError):
    def __init__(self, token):
        line, column = token.position
        message = f"InvalidAddExpression: ({line}, {column}): Niepoprawne wyrażenie po operatorze dodawania/odejmowania: '{token.value}'."
        super().__init__(message)
