from http.client import BAD_REQUEST, OK
from loguru import logger
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
            logger.info("Executing UserDiskSpace...")
            self._model_token.token = token

            logger.info("Getting user information from PostgreSQL...")
            db = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            await db.execute()
            settings = await self._settings.get()

            logger.info("Retrieving disk space settings...")
            self.__total_disk_space = settings['disk_space_per_user']
            self._s3.set_bucket_name(db.response.login)
            logger.info("Calculating user disk space...")
            self.__user_disk_space = self._s3.bucket().get_size
            self._status_code = OK
            logger.info("UserDiskSpace executed successfully.")
            return
        except ValueError as e:
            logger.error("ValueError occurred: {}", e)
            self._status_code = BAD_REQUEST
        finally:
            logger.info("Closing database connection...")
            await self._connection.close()
            logger.info("Database connection closed.")
