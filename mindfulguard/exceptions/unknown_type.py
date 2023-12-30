class ExceptionUnknownType(Exception):
    def __init__(self, message="Unknown Type"):
        super().__init__(message)