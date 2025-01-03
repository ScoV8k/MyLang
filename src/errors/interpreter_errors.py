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