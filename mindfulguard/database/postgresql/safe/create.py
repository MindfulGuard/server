from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection

class PostgreSqlSafeCreate(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_safe: ModelSafe
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__model_safe: ModelSafe = model_safe
    
    async def execute(self) -> None:
        value: int = await self._connection.connection.fetchval('''
        SELECT create_safe($1, $2, $3)
        ''',
        self.__model_token.token,
        self.__model_safe.name,
        self.__model_safe.description
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