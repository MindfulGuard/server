from http.client import OK, INTERNAL_SERVER_ERROR, UNAUTHORIZED
import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from loguru import logger
import time

class PostgreSqlItemsUpdate(PostgreSqlQueriesBase):
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
        logger.debug("Executing SQL query to update item...")

        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT update_item($1, $2, $3, $4, $5, $6, $7, $8);
            ''',
            self.__model_token.token,
            self.__model_record.safe_id,
            self.__model_record.id,
            self.__model_record.title,
            self.__model_record.item,
            self.__model_record.notes,
            self.__model_record.tags,
            self.__model_record.category
            )
            if value == 0:
                self._status_code = OK
                logger.debug("Item updated successfully.")
                return
            elif value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access during item update operation.")
                return
            elif value == -2:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Internal server error occurred during item update operation.")
                return
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Unknown error occurred during item update operation.")
                return
        except asyncpg.exceptions.ForeignKeyViolationError:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error("Foreign key violation error occurred during item update operation.")
        except asyncpg.exceptions.UniqueViolationError:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error("Unique violation error occurred during item update operation.")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Item update execution time: {} seconds", execution_time)
