class ErrorManager:
    errors: list[Exception]

    def __init__(self) -> None:
        self.lexer_errors = []
        self.parser_errors = []

    def get_all_lexer_errors(self) -> list:
        return self.lexer_errors
    
    def add_lexer_error(self, error: Exception) -> None:
        self.lexer_errors.append(error)

    def get_all_parser_errors(self) -> list:
        return self.parser_errors
    
    def add_parser_error(self, error: Exception) -> None:
        self.parser_errors.append(error)
