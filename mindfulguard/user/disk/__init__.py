from mindfulguard.user.disk.space import UserDiskSpace

class UserDisk:
    def space(self) -> UserDiskSpace:
        return UserDiskSpace()