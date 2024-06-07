from http.client import BAD_REQUEST, OK
from typing import Any
from loguru import logger
from mindfulguard.classes.admin.base import AdminBase
from mindfulguard.api_configuration.public import ConfigurationPublic
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
from redis.commands.json.path import Path

class AdminConfigurationGet(AdminBase):
    def __init__(self) -> None:
        super().__init__()
        self.__public_configuration = ConfigurationPublic()
        self.__pgsql_auth_admin = PostgreSqlAuthentication(self._connection)
        self.__cache_name = f'{self._redis.CACHE_NAME_SETTINGS}:admin'
        
    @property
    def response(self) -> dict[str, Any]:
        return self._response

    async def execute(self, token: str) -> None:
        try:
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

            logger.info("Fetching configuration from cache...")
            self._response = self._redis.client().connection.json().get(self.__cache_name)
            if self._response:
                logger.info("Configuration found in cache.")
                self._status_code = db.status_code
                return

            logger.info("Configuration not found in cache, fetching from database...")
            await self.__public_configuration.execute()
            response: dict[str, Any] = self.__public_configuration.response
            response['registration'] = self.__public_configuration.settings['registration']
            response['scan_time_routines_tokens'] = self.__public_configuration.settings['scan_time_routines_tokens']
            response['scan_time_routines_users'] = self.__public_configuration.settings['scan_time_routines_users']
            response['confirmation_period'] = self.__public_configuration.settings['confirmation_period']
            response['disk_space_per_user'] = self.__public_configuration.settings['disk_space_per_user']

            self._response = response

            logger.debug("Data: {}", self._response)

            logger.info("Caching fetched configuration...")
            self._redis.client().connection.json().set(
                self.__cache_name,
                Path.root_path(),
                self._response
            )
            self._redis.client().connection.expire(self.__cache_name, 3600)
            self._status_code = OK
            logger.info("Configuration cached successfully.")
            return
        except ValueError as e:
            logger.error("An error occurred: {}", e)
            self._status_code = BAD_REQUEST
        finally:
            logger.info("Closing database connection...")
            await self._connection.close()
