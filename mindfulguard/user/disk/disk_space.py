from http.client import BAD_REQUEST, OK
from mindfulguard.classes.user.base import UserBase

class UserDiskSpace(UserBase):
    def __init__(self) -> None:
        super().__init__()
        self.__total_disk_space: int
        self.__user_disk_space: int

    @property
    def total_disk_space(self) -> int:
        return self.__total_disk_space
    
    @property
    def user_disk_space(self) -> int:
        return self.__user_disk_space

    async def execute(self, token: str) -> None:
        try:
            self._model_token.token = token

            db = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            await db.execute()
            await self._settings.execute()

            self.__total_disk_space = self._settings.response['disk_space_per_user']
            self._s3_bucket_name = db.response.login
            self.__user_disk_space = self._s3.bucket().get_size
            self._status_code = OK
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()