from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlSafeUpdate(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_safe: ModelSafe
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__model_safe: ModelSafe = model_safe
    
    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Updating safe information...")

        try:
            value = await self._connection.connection.fetchval('''
            SELECT update_safe($1,$2,$3,$4)
            ''',
            self.__model_token.token,
            self.__model_safe.id,
            self.__model_safe.name,
            self.__model_safe.description
            )

            if value == 0:
                self._status_code = OK
                logger.debug("Safe information updated successfully.")
                return
            elif value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access to update safe information.")
                return
            elif value == -2:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("An error occurred while updating safe information.")
                return
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("An unknown error occurred while updating safe information.")
                return
        except Exception as e:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error(f"An error occurred while updating safe information: {e}")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Safe update execution time: {} seconds", execution_time)
