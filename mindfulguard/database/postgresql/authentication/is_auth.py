from http.client import OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlIsAuth(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token

    async def execute(self) -> None:
        value: bool = await self._connection.connection.fetchval('''
        SELECT active_token($1);
        ''', 
        self.__model_token.token
        )
        if value:
            self._status_code = OK
            return
        else:
            self._status_code = UNAUTHORIZED
            return