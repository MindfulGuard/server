from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlItemsDelete(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_record: ModelRecord
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__model_record: ModelRecord = model_record

    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query to delete item...")

        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT delete_item($1, $2, $3);
            ''',
            self.__model_token.token,
            self.__model_record.safe_id,
            self.__model_record.id
            )
            if value == 0:
                self._status_code = OK
                logger.debug("Item deleted successfully.")
            elif value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access during item deletion.")
            elif value == -2:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Internal server error occurred during item deletion.")
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Unknown error occurred during item deletion.")
        except asyncpg.exceptions.ForeignKeyViolationError:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error("Foreign key violation error occurred during item deletion.")
        except Exception as e:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error("An unexpected error occurred during item deletion: {}", e)
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Item deletion execution time: {} seconds", execution_time)
            logger.debug("Execution of item deletion query completed.")
