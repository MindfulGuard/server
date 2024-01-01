from mindfulguard.admin.configuration import AdminConfiguration
from mindfulguard.admin.users import AdminUsers

class Admin:
    def users(self) -> AdminUsers:
        return AdminUsers()
    
    def configuration(self) -> AdminConfiguration:
        return AdminConfiguration()