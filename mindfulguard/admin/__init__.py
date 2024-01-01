from mindfulguard.admin.configuration import AdminConfiguration

class Admin:
    def users(self):
        from mindfulguard.admin.users import AdminUsers
        return AdminUsers()
    
    def configuration(self) -> AdminConfiguration:
        return AdminConfiguration()