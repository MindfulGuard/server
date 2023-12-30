from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.items.model_record_extend import ModelRecordExtend


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
                return
            elif value == -1:
                self._status_code = UNAUTHORIZED
                return
            elif value == -2:
                self._status_code = INTERNAL_SERVER_ERROR
                return
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                return
        except asyncpg.exceptions.ForeignKeyViolationError:
            self._status_code = INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError:
            self._status_code = INTERNAL_SERVER_ERROR