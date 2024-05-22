from http.client import BAD_REQUEST, OK
from mindfulguard.classes.safe.base import SafeBase
from loguru import logger

class Update(SafeBase):
    def __init__(self) -> None:
        super().__init__()

    async def execute(
        self,
        token: str,
        safe_id: str,
        name: str,
        description: str
    ) -> None:
        logger.debug("Executing 'execute' method to update safe: {} with name: {} and description: {}", safe_id, name, description)
        try:
            self._model_token.token = token
            self._model_safe.id = safe_id
            self._model_safe.name = name
            self._model_safe.description = description
            db = self._pgsql_safe.update(self._model_token, self._model_safe)
            db_user_info = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            await db.execute()
            await db_user_info.execute()
            if db.status_code == OK and db_user_info.status_code == OK:
                for i in self._redis.client().connection.scan_iter(
                    f'{db_user_info.response.login}:{self._redis.PATH_SAFE_ALL_ITEM}'
                ):
                    self._redis.client().connection.delete(i)
                logger.debug("Successfully updated safe: {}", safe_id)
            self._status_code = db.status_code
            return
        except ValueError as e:
            self._status_code = BAD_REQUEST
            logger.error("ValueError occurred: {}", e)
        except Exception as e:
            logger.error("An error occurred while updating safe: {}", e)
        finally:
            await self._connection.close()
            logger.debug("Database connection closed.")
