from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.items.model_record_extend import ModelRecordExtend
from loguru import logger
import time

class PostgreSqlItemsMove(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_record_extend: ModelRecordExtend
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__model_record_extend: ModelRecordExtend = model_record_extend

    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Executing SQL query to move item to new safe...")

        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT move_item_to_new_safe($1, $2, $3, $4);
            ''',
            self.__model_token.token,
            self.__model_record_extend.old_safe_id,
            self.__model_record_extend.new_safe_id,
            self.__model_record_extend.id
            )
            if value == 0:
                self._status_code = OK
                logger.debug("Item moved to new safe successfully.")
                return
            elif value == -1:
                self._status_code = UNAUTHORIZED
                logger.warning("Unauthorized access during item move operation.")
                return
            elif value == -2:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Internal server error occurred during item move operation.")
                return
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                logger.error("Unknown error occurred during item move operation.")
                return
        except asyncpg.exceptions.ForeignKeyViolationError:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error("Foreign key violation error occurred during item move operation.")
        except asyncpg.exceptions.UniqueViolationError:
            self._status_code = INTERNAL_SERVER_ERROR
            logger.error("Unique violation error occurred during item move operation.")
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Item move execution time: {} seconds", execution_time)
