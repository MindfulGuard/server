from http.client import FORBIDDEN, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlIsAuthAdmin(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token = model_token

    async def execute(self) -> None:
        value: int = await self._connection.connection.fetchval('''
            SELECT active_token_admin($1);
        ''',
        self.__model_token.token
        )
        
        if value == -1:
            self._status_code = UNAUTHORIZED
            return
        elif value == -2:
            self._status_code = FORBIDDEN
            return
        else:
            self._status_code = OK
            return