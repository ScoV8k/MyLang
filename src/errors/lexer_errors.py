class InvalidTokenError(Exception):
    def __init__(self, position, char):
        line, column = position
        text = f"Error in line {line}, column {column}: Unexpected character \'{char}\'"
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message