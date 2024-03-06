from http.client import OK, UNAUTHORIZED
import json
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.authentication.is_auth import PostgreSqlIsAuth
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlItemsGet(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__pgsql_is_auth = PostgreSqlIsAuth(self._connection, model_token)

    class __Iterator:
        def __init__(self, pgsql_response: list):
            self.__pgsql_response: list = pgsql_response
            self.__model_record = ModelRecord()
            self.__i: int = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.__i < len(self.__pgsql_response):
                self.__model_record.id = self.__pgsql_response[self.__i]['r_id']
                self.__model_record.safe_id = self.__pgsql_response[self.__i]['s_id']
                self.__model_record.title = self.__pgsql_response[self.__i]['r_title']
                self.__model_record.item = json.loads(self.__pgsql_response[self.__i]['r_item'])
                self.__model_record.created_at = self.__pgsql_response[self.__i]['r_created_at']
                self.__model_record.updated_at = self.__pgsql_response[self.__i]['r_updated_at']
                self.__model_record.category = self.__pgsql_response[self.__i]['r_category']
                self.__model_record.notes = self.__pgsql_response[self.__i]['r_notes']
                self.__model_record.tags = self.__pgsql_response[self.__i]['r_tags']
                self.__model_record.favorite = self.__pgsql_response[self.__i]['r_favorite']
                self.__i += 1
                return self.__model_record
            else:
                raise StopIteration

    @property
    def response(self) -> __Iterator:
        return self._response

    async def execute(self) -> None:
        await self.__pgsql_is_auth.execute()
        if self.__pgsql_is_auth.status_code == UNAUTHORIZED:
            self._status_code = self.__pgsql_is_auth.status_code
            return
        
        values = await self._connection.connection.fetch('''
        SELECT s.s_id, r.r_id, r.r_title, r.r_item, r.r_category, r.r_notes, r.r_tags, r.r_favorite, r.r_created_at, r.r_updated_at
        FROM r_records AS r
        JOIN s_safes AS s ON s.s_id = r.r_s_id
        JOIN t_tokens AS t ON t.t_u_id = r.r_u_id
        WHERE t.t_token = $1
        AND active_token($1) = True
        ORDER BY r.r_updated_at DESC;
        ''',
        self.__model_token.token
        )
        self._response = self.__Iterator(values)
        self._status_code = OK
        return