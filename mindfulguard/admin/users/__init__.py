from mindfulguard.admin.users.get_by_page import AdminUsersGetByPage
from mindfulguard.admin.users.search_users import AdminUsersSearchUsers


class AdminUsers:
    def get_by_page(self) -> AdminUsersGetByPage:
        return AdminUsersGetByPage()
    
    def search_users(self) -> AdminUsersSearchUsers:
        return AdminUsersSearchUsers()