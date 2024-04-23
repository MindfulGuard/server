from fastapi import Response
from mindfulguard.classes.admin.configuration import AdminConfiguration
from mindfulguard.classes.admin.users import AdminUsers
from mindfulguard.classes.responses import HttpResponse

class AdminClass:
    def __init__(self, response: Response) -> None:
        from mindfulguard.admin import Admin
        self.__http_response = HttpResponse()
        self.__response: Response = response
        self.__admin_class = Admin()

    def users(self) -> AdminUsers:
        return AdminUsers(
            self.__response,
            self.__http_response,
            self.__admin_class
        )
    
    def configuration(self):
        return AdminConfiguration(
            self.__response,
            self.__http_response,
            self.__admin_class
        )