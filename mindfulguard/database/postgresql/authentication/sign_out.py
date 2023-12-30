from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlSignOut(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token

    async def execute(self) -> None:
        value: int = await self._connection.connection.fetchval('''
        SELECT sign_out($1, $2);
        ''',
        self.__model_token.token,
        self.__model_token.id
        )
        
        if value == 0:
            self._status_code = OK
            return
        elif value == -1:
            self._status_code = UNAUTHORIZED
            return
        elif value == -2:
            self._status_code = NOT_FOUND
            return
        else:
            self._status_code = INTERNAL_SERVER_ERROR
            return