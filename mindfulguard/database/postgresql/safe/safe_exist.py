from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlSafeExist(PostgreSqlQueriesBase):
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
        logger.debug("Checking if safe exists...")

        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT safe_and_element_exists($1, $2);
            ''',
            self.__model_token.token,
            self.__model_safe.id
            )

            if value == 0:
                self._status_code = OK
                logger.debug("Safe exists.")
                return
            elif value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access to check safe existence.")
                return
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("An error occurred while checking safe existence.")
                return
        except Exception as e:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error(f"An error occurred while checking safe existence: {e}")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Safe existence check execution time: {} seconds", execution_time)
