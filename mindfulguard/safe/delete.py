from http.client import BAD_REQUEST, OK
from mindfulguard.classes.safe.base import SafeBase
from loguru import logger

class Delete(SafeBase):
    def __init__(self) -> None:
        super().__init__()
    
    async def execute(
        self,
        token: str,
        safe_id: str,
    ) -> None:
        logger.debug("Executing 'execute' method to delete safe with ID: {}", safe_id)
        try:
            self._model_token.token = token
            self._model_safe.id = safe_id
            db = self._pgsql_safe.delete(self._model_token, self._model_safe)
            db_user_info = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            logger.debug("Database connection opened for delete operation.")
            await db.execute()
            await db_user_info.execute()
            self._status_code = db.status_code
            if db.status_code == OK and db_user_info.status_code == OK:
                self._s3.set_bucket_name(db_user_info.response.login)
                object_list = [obj.object_name for obj in self._s3.object().get_all_objects(f'{self._s3.CONTENT_PATH}/{safe_id}/')]
                self._s3.object().delete_objects(object_list) # type: ignore
                logger.debug("Objects related to safe ID: {} deleted from S3 bucket.", safe_id)
                for i in self._redis.client().connection.scan_iter(
                    f'{db_user_info.response.login}:{self._redis.PATH_SAFE_ALL_ITEM}'
                ):
                    self._redis.client().connection.delete(i)
                logger.debug("Redis cache for user: {} cleared.", db_user_info.response.login)
        except ValueError as e:
            self._status_code = BAD_REQUEST
            logger.error("ValueError occurred: {}", e)
        finally:
            await self._connection.close()
            logger.debug("Database connection closed.")
