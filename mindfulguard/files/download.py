from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, OK
from loguru import logger

from mindfulguard.classes.files.base import FilesBase


class Download(FilesBase):
    def __init__(self) -> None:
        super().__init__()
        self.__data: bytes = b''
        self.__name: str = ''

    @property
    def data(self) -> bytes:
        return self.__data
    
    @property
    def name(self) -> str:
        return self.__name

    async def execute(
        self,
        token: str,
        safe_id: str,
        object_name: str
    ) -> None:
        try:
            self._model_token.token = token
            self._model_safe.id = safe_id
            db = self._pgsql_user.get_information(self._model_token)

            await self._connection.open()
            await db.execute()

            if db.status_code != OK:
                self._status_code = db.status_code
                return
            
            self._s3.set_bucket_name(db.response.login)
            s3 = self._s3.object().get_object(
                f"{self._s3.CONTENT_PATH}/{self._model_safe.id}/{object_name}"
            )
            if s3 is None:
                self._status_code = INTERNAL_SERVER_ERROR
                return

            self.__data = s3[0]
            self._name = s3[1]
            self._status_code = db.status_code
            logger.info(f"Downloaded object: {self._name}")
            return
        except ValueError as e:
            logger.info("An error occurred: {}", e)
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()