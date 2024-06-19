from http.client import BAD_REQUEST, OK

import grpc
from mindfulguard.classes.admin.base import AdminBase
from mindfulguard.classes.models.settings import ModelSettings
from loguru import logger

from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
from mindfulguard.grpc.client.dynamic_configurations.methods import GrpcDynamicConfigurationsMethods
from mindfulguard.settings import Settings

class AdminConfigurationUpdate(AdminBase):
    def __init__(self) -> None:
        super().__init__()
        self.__model_settings = ModelSettings()
        self.__pgsql_auth_admin = PostgreSqlAuthentication(self._connection)
        self.__settings = Settings()
        self.__cache_name: str = self._redis.CACHE_NAME_SETTINGS

    async def execute(self, token: str, key: str, value: str) -> None:
        try:
            logger.info("Initializing configuration update...")

            self._model_token.token = token
            logger.info("Checking admin authentication...")
            db = self.__pgsql_auth_admin.is_auth_admin(
                self._model_token
            )
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            if db.status_code != OK:
                logger.warning(f"Admin authentication failed with status code: {db.status_code}")
                return

            self.__model_settings.key = key
            self.__model_settings.value = value

            logger.info("Updating configuration in the dynamic configurations service...")

            self._status_code = await self.__settings.update(self.__model_settings.key, self.__model_settings.value)
        except ValueError as e:
            logger.error("An error occurred: {}", e)
            self._status_code = BAD_REQUEST
        finally:
            logger.info("Closing database connection...")
            await self._connection.close()
