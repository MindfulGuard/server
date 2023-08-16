from typing import Any
from mypass.core.languages.package_reader import Files

class Language:
    def __init__(self):
        self.__message = Files()
    def data_not_valid(self)->dict[str,Any]:
        return self.__message.get("data_not_valid")
    def registration_not_allowed(self)->dict[str,Any]:
        return self.__message.get("registration_not_allowed")
    def registration_was_successful(self)->dict[str,Any]:
        return self.__message.get("registration_was_successful")
    def service_is_not_available(self)->dict[str,Any]:
        return self.__message.get("service_is_not_available")
    def server_error(self)->dict[str,Any]:
        return self.__message.get("server_error")
    def user_already_exists(self)->dict[str,Any]:
        return self.__message.get("user_already_exists")