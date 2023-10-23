from typing import Any
from mindfulguard.core.languages import Language

"""
Popular json responses are stored here
"""

class Responses:
    def __init__(self,language:Language):
        """
        Params:
        language type(Language)
        """
        self.__language = language

    def service_is_not_available(self)-> dict[str, dict[str, Any]]:
        return {"msg":self.__language.service_is_not_available()}
    def data_not_valid(self)-> dict[str, dict[str, Any]]:
        return {"msg":self.__language.data_not_valid()}
    def unauthorized(self)-> dict[str, dict[str, Any]]:
        return {"msg":self.__language.unauthorized()}
    def forbidden(self)-> dict[str, dict[str, Any]]:
        return {"msg":self.__language.access_denied()}
    def server_error(self)-> dict[str, dict[str, Any]]:
        return {"msg":self.__language.server_error()}