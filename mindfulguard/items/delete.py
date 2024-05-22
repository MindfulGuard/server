from http.client import BAD_REQUEST, OK
from loguru import logger
from mindfulguard.classes.items.base import ItemsBase


class Delete(ItemsBase):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Delete class initialized.")

    async def execute(self, token: str, safe_id: str, record_id: str) -> None:
        logger.debug("Execute method called with token: {}, safe_id: {}, record_id: {}", token, safe_id, record_id)
        try:
            self._model_token.token = token
            self._model_record.id = record_id
            self._model_record.safe_id = safe_id

            logger.debug("Model token and record set. Token: {}, Record ID: {}, Safe ID: {}", token, record_id, safe_id)

            db = self._pgsql_items.delete(self._model_token, self._model_record)
            await self._connection.open()
            logger.debug("Database connection opened for delete operation.")

            db_user_info = self._pgsql_user.get_information(self._model_token)
            await db.execute()
            await db_user_info.execute()
            self._status_code = db.status_code
            logger.debug("Database delete operation executed with status code: {}", db.status_code)

            if db.status_code == OK and db_user_info.status_code == OK:
                for i in self._redis.client().connection.scan_iter(
                    f'{db_user_info.response.login}:{self._redis.PATH_SAFE_ALL_ITEM}'
                ):
                    self._redis.client().connection.delete(i)
                logger.debug("Redis cache cleared for user: {}", db_user_info.response.login)
            return
        except ValueError as e:
            self._status_code = BAD_REQUEST
            logger.error("ValueError occurred: {}", e)
        finally:
            await self._connection.close()
            logger.debug("Database connection closed.")
