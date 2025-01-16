class InterpreterError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
    
    def __eq__(self, other):
        if not isinstance(other, InterpreterError):
            return False
        return self.message == other.message


class RecursionLimitExceeded(InterpreterError):
    def __init__(self):
        message = f"RecursionLimitExceeded."
        super().__init__(message)


class InvalidFunctionCall(InterpreterError):
    def __init__(self, id) -> None:
        super().__init__(f"{id} is not a function.")


class FunctionDoesNotExist(InterpreterError):
    def __init__(self, id) -> None:
        super().__init__(f"Function: {id} does not exist")


class AndOperationError(InterpreterError):
    def __init__(self, x, term):
        super().__init__()


class OrOperationError(InterpreterError):
    def __init__(self, x, term):
        super().__init__()


class BreakException(InterpreterError):
    """Wyjątek używany do obsługi instrukcji break w pętlach."""
    pass

class RecursionLimitExceeded(InterpreterError):
    def __init__(self):
        super().__init__()

class MainFunctionRequired(InterpreterError):
    def __init__(self, *args: object) -> None:
        super().__init__("Main function is required")

class ReturnInMainFunctionRequired(InterpreterError):
    def __init__(self) -> None:
        super().__init__("Wymagana instrukcja return w funkcji main()")

class TypeMismatchError(InterpreterError):
    def __init__(self) -> None:
        super().__init__("Wymagana instrukcja return w funkcji main()")

class DeclarationError(InterpreterError):
    def __init__(self, variable) -> None:
        super().__init__(f"Zmienna {variable} została juz zadeklarowana.")

class VariableError(InterpreterError):
    def __init__(self, variable) -> None:
        super().__init__(f"Zmienna {variable} nie została juz zadeklarowana.")

# dodać drugi jak jest jak nie ma 


class AssignmentError(InterpreterError):
    def __init__(self, variable) -> None:
        super().__init__(f"Zmienna {variable} nie została wcześniej zadeklarowana.")

class FunctionError(InterpreterError):
    def __init__(self, variable) -> None:
        super().__init__(f"Funkcja {variable} nie została wcześniej zadeklarowana.")

class IdentifierInObjectAccessError(InterpreterError):
    def __init__(self, name) -> None:
        super().__init__(f"Nie można wywołać dostępu do zmiennej {name} w ten sposób")

class NegationError(InterpreterError):
    def __init__(self, position, type, element) -> None:
        line, column = position
        message = f"NegationError ({line}, {column}): Nie mozna wykonac operacji negacji typu \"{type}\" na elemencie \"{element}\""
        super().__init__(message)
