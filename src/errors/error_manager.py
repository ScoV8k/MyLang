class ErrorManager:
    errors: list[Exception]

    def __init__(self) -> None:
        self.errors = []

    def get_all_errors(self) -> list:
        return self.errors
    
    def add_error(self, error: Exception) -> None:
        self.errors.append(error)
