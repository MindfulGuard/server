class ExceptionIncorrectParameters(Exception):
    def __init__(self, message="Incorrect parameters"):
        super().__init__(message)