from http.client import BAD_REQUEST, OK
from mindfulguard.classes.admin.base import AdminBase
from mindfulguard.classes.models.settings import ModelSettings
from loguru import logger


class AdminConfigurationUpdate(AdminBase):
    def __init__(self) -> None:
        super().__init__()
        self.__model_settings = ModelSettings()
        self.__cache_name: str = self._redis.CACHE_NAME_SETTINGS

    async def execute(self, token: str, key: str, value: str) -> None:
        try:
            logger.info("Initializing configuration update...")
            self._model_token.token = token
            self.__model_settings.key = key
            self.__model_settings.value = value

            logger.info("Updating configuration in the database...")
            db = self._pgsql_admin.update_configuration(
                self._model_token,
                self.__model_settings
            )
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            if db.status_code == OK:
                logger.info("Configuration update successful. Clearing cache...")
                for i in self._redis.client().connection.scan_iter(f'{self.__cache_name}:*'):
                    self._redis.client().connection.delete(i)
                logger.info("Cache cleared.")
            return
        except ValueError as e:
            logger.error("An error occurred: {}", e)
            self._status_code = BAD_REQUEST
        finally:
            logger.info("Closing database connection...")
            await self._connection.close()
