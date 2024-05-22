from http.client import FORBIDDEN, INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.settings import ModelSettings
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlAdminConfigurationUpdate(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_settings: ModelSettings
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__model_settings: ModelSettings = model_settings

    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query for admin configuration update...")
        
        try:
            response: int = await self._connection.connection.fetchval('''
            SELECT update_settings_admin($1,$2,$3);
            ''',
            self.__model_token.token,
            self.__model_settings.key,
            self.__model_settings.value
            )
            
            logger.debug("SQL query executed successfully with response: {}.", response)

            if response == 0:
                self._status_code = OK
                logger.debug("Admin configuration updated successfully.")
            elif response == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access for admin configuration update.")
            elif response == -2:
                self._status_code = FORBIDDEN
                logger.warning("Forbidden access for admin configuration update.")
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Internal server error occurred while updating admin configuration.")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Admin configuration update execution time: {} seconds", execution_time)
            
            logger.debug("Admin configuration update execution completed.")
