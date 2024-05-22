from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlSignOut(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token

    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query to sign out user...")

        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT sign_out($1, $2);
            ''',
            self.__model_token.token,
            self.__model_token.id
            )
            
            if value == 0:
                self._status_code = OK
                logger.debug("User signed out successfully.")
            elif value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access for user sign out.")
            elif value == -2:
                self._status_code = NOT_FOUND
                logger.warning("Token not found for user sign out.")
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Internal server error occurred during user sign out.")
        except Exception as e:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.exception("An error occurred during user sign out: {}", e)
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Sign out execution time: {} seconds", execution_time)
            logger.debug("Execution of sign out query completed.")
