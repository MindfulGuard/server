from http.client import FORBIDDEN, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlIsAuthAdmin(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token = model_token

    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query to check admin authentication...")

        try:
            value: int = await self._connection.connection.fetchval('''
                SELECT active_token_admin($1);
            ''',
            self.__model_token.token
            )
            
            if value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Admin authentication failed: Unauthorized.")
            elif value == -2:
                self._status_code = FORBIDDEN
                logger.warning("Admin authentication failed: Forbidden.")
            else:
                self._status_code = OK
                logger.debug("Admin authentication successful.")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Admin authentication execution time: {} seconds", execution_time)
