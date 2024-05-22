from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, OK
from loguru import logger
from mindfulguard.classes.files.base import FilesBase


class Delete(FilesBase):
    def __init__(self) -> None:
        super().__init__()

    async def execute(self, token: str, safe_id: str, files: list[str]) -> None:
        try:
            if len(files) == 0:
                logger.error("No files provided for deletion")
                self._status_code = BAD_REQUEST
                return

            self._model_token.token = token
            self._model_safe.id = safe_id

            db = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            await db.execute()

            if db.status_code != OK:
                logger.error(f"Failed to retrieve information from database. Status code: {db.status_code}")
                self._status_code = db.status_code
                return
            
            self._s3.set_bucket_name(db.response.login)
            s3 = self._s3.object().delete_objects(
                files,
                prefix_object_name_ = f"{self._s3.CONTENT_PATH}/{self._model_safe.id}/"
            )
            if s3:
                logger.info("Files deleted successfully from S3")
                self._status_code = OK
                for i in self._redis.client().connection.scan_iter(
                    f'{db.response.login}:{self._redis.PATH_SAFE_ALL_ITEM}'
                ):
                    self._redis.client().connection.delete(i)
                logger.info("Cache cleared for safe items")
                return
            else:
                logger.error("Failed to delete files from S3")
                self._status_code = INTERNAL_SERVER_ERROR
                return
        except ValueError:
            logger.info("Invalid input data provided")
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()
            logger.info("Database connection closed")
