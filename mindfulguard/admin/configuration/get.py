from http.client import BAD_REQUEST, OK
from typing import Any
from loguru import logger
from mindfulguard.classes.admin.base import AdminBase
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
from redis.commands.json.path import Path
from mindfulguard.settings import Settings

class AdminConfigurationGet(AdminBase):
    def __init__(self) -> None:
        super().__init__()
        self.__settings = Settings()
        self.__pgsql_auth_admin = PostgreSqlAuthentication(self._connection)
        
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

            self._response =  await self.__settings.get()
        except ValueError as e:
            logger.error("An error occurred: {}", e)
            self._status_code = BAD_REQUEST
        finally:
            logger.info("Closing database connection...")
            await self._connection.close()
