from fastapi import Response
from mindfulguard.classes.admin.configuration import AdminConfiguration
from mindfulguard.classes.admin.users import AdminUsers
from mindfulguard.classes.responses import Responses

class AdminClass:
    def __init__(self, response: Response) -> None:
        from mindfulguard.admin import Admin
        self.__responses = Responses()
        self.__response: Response = response
        self.__admin_class = Admin()

    def users(self) -> AdminUsers:
        return AdminUsers(
            self.__response,
            self.__responses,
            self.__admin_class
        )
    
    def configuration(self):
        return AdminConfiguration(
            self.__response,
            self.__responses,
            self.__admin_class
        )