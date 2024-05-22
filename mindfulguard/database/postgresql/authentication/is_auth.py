from http.client import OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlIsAuth(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token

    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query to check authentication...")

        try:
            value: bool = await self._connection.connection.fetchval('''
            SELECT active_token($1);
            ''', 
            self.__model_token.token
            )
            if value:
                self._status_code = OK
                logger.debug("Authentication successful.")
            else:
                self._status_code = UNAUTHORIZED
                logger.warning("Authentication failed: Unauthorized.")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Authentication execution time: {} seconds", execution_time)
            logger.debug("Execution of authentication query completed.")
