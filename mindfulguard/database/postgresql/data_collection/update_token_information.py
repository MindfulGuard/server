from http.client import OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlUpdateTokenInformation(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token

    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query to update token information...")

        try:
            value = await self._connection.connection.fetchval('''
            SELECT update_token_info($1, $2, $3);
            ''',
            self.__model_token.token,
            self.__model_token.device,
            self.__model_token.last_ip
            )
            if value:
                self._status_code = OK
                logger.debug("Token information updated successfully.")
            else:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access during token information update.")
        except Exception as e:
            self._status_code = UNAUTHORIZED
            logger.exception("An error occurred during token information update: {}", e)
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Token information update execution time: {} seconds", execution_time)
            logger.debug("Execution of token information update query completed.")
