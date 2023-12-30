from http.client import OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlUpdateTokenInformation(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token

    async def execute(self) -> None:
        value = await self._connection.connection.fetchval('''
        SELECT update_token_info($1, $2, $3);
        ''',
        self.__model_token.token,
        self.__model_token.device,
        self.__model_token.last_ip
        )
        if value:
            self._status_code = OK
            return
        else:
            self._status_code = UNAUTHORIZED
            return