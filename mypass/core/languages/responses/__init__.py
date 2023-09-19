from mypass.core.languages import Language

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

    def service_is_not_available(self):
        return {"msg":self.__language.service_is_not_available()}
    def data_not_valid(self):
        return {"msg":self.__language.data_not_valid()}
    def unauthorized(self):
        return {"msg":self.__language.unauthorized()}
    def server_error(self):
        return {"msg":self.__language.server_error()}