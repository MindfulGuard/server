from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlSafeDelete(PostgreSqlQueriesBase):
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
        logger.debug("Executing SQL query to delete safe...")

        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT delete_safe($1, $2);
            ''',
            self.__model_token.token,
            self.__model_safe.id
            )
            if value == 0:
                self._status_code = OK
                logger.debug("Safe deleted successfully.")
                return
            elif value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access during safe deletion.")
                return
            elif value == -2:
                self._status_code = NOT_FOUND
                logger.warning("Safe not found during deletion.")
                return
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Internal server error occurred during safe deletion.")
                return
        except Exception as e:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error(f"An error occurred during safe deletion: {e}")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Safe deletion execution time: {} seconds", execution_time)
