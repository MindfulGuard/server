from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlSafeCreate(PostgreSqlQueriesBase):
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
        logger.debug("Executing SQL query to create safe...")

        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT create_safe($1, $2, $3)
            ''',
            self.__model_token.token,
            self.__model_safe.name,
            self.__model_safe.description
            )
            if value == 0:
                self._status_code = OK
                logger.debug("Safe created successfully.")
                return
            elif value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access during safe creation.")
                return
            elif value == -2:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Internal server error occurred during safe creation.")
                return
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Unknown error occurred during safe creation.")
                return
        except Exception as e:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error(f"An error occurred during safe creation: {e}")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Safe creation execution time: {} seconds", execution_time)
