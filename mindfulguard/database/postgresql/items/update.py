from http.client import OK, INTERNAL_SERVER_ERROR, UNAUTHORIZED
import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


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