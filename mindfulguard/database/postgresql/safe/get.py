from http.client import OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.authentication.is_auth import PostgreSqlIsAuth
from mindfulguard.database.postgresql.connection import PostgreSqlConnection

class PostgreSqlSafeGet(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__pgsql_is_auth = PostgreSqlIsAuth(self._connection, model_token)

    class _ModelSafeExtend(ModelSafe):
        def __init__(self):
            super().__init__()
            self.__count_items: int
        
        @property
        def id(self) -> str:
            return self._id

        @id.setter
        def id(self, value: str) -> None:
            self._id = value

        @property
        def count_items(self) -> int:
            return self.__count_items
        
        @count_items.setter
        def count_items(self, value: int) -> None:
            self.__count_items = value

    class __Iterator:
        def __init__(self, pgsql_response: list):
            self.__pgsql_response: list = pgsql_response
            self.__model_safe_extend = PostgreSqlSafeGet._ModelSafeExtend()
            self.__i: int = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.__i < len(self.__pgsql_response):
                self.__model_safe_extend.id = self.__pgsql_response[self.__i]['s_id']
                if not self.__model_safe_extend.id:
                    self.__model_safe_extend.id = ''
                    raise StopIteration
                self.__model_safe_extend.name = self.__pgsql_response[self.__i]['s_name']
                self.__model_safe_extend.description = self.__pgsql_response[self.__i]['s_description']
                self.__model_safe_extend.created_at = self.__pgsql_response[self.__i]['s_created_at']
                self.__model_safe_extend.updated_at = self.__pgsql_response[self.__i]['s_updated_at']
                self.__model_safe_extend.count_items = self.__pgsql_response[self.__i]['r_count']
                self.__i += 1
                return self.__model_safe_extend
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
        SELECT s.s_id, s.s_name, s.s_description, s.s_created_at, s.s_updated_at, COUNT(r.r_id) AS r_count
        FROM s_safes AS s
        JOIN t_tokens AS t ON t.t_u_id = s.s_u_id
        LEFT JOIN r_records AS r ON r.r_s_id = s.s_id
        WHERE t.t_token = $1
        AND active_token($1) = True
        GROUP BY s.s_id, s.s_name, s.s_description, s.s_created_at, s.s_updated_at;
        ''',
        self.__model_token.token
        )
        
        self._response = self.__Iterator(values)
        self._status_code = OK
        return