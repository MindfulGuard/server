from mindfulguard.user.disk import UserDisk
from mindfulguard.user.information import UserInformation
from mindfulguard.user.settings import UserSettings

class User:
    def disk(self) -> UserDisk:
        return UserDisk()
    
    def information(self) -> UserInformation:
        return UserInformation()
    
    def settings(self) -> UserSettings:
        return UserSettings()