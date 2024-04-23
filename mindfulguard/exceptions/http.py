class InvalidHttpMethod(Exception):
    def __init__(self, message="Invalid HTTP method."):
        super().__init__(message)

class InvalidUrlPath(Exception):
    def __init__(self, message="Invalid url path."):
        super().__init__(message)

class InvalidHttpStatusCode(Exception):
    def __init__(self, message="Invalid HTTP status code."):
        super().__init__(message)