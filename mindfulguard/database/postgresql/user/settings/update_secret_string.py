from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.user.settings.model_user_extend import ModelUserExtend


class PostgreSqlUserSettingsUpdateSecretString(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_user_extend: ModelUserExtend
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__model_user_extend: ModelUserExtend =  model_user_extend
    
    def secret_code(self):
        return PostgreSqlUserSettingsSecretCode(
            self._connection,
            self.__model_token,
            self.__model_user_extend
        )

    async def execute(self) -> None:
        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT update_secret_string($1, $2, $3);
            ''',
            self.__model_token.token,
            self.__model_user_extend.old_secret_string,
            self.__model_user_extend.new_secret_string
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
        except asyncpg.exceptions.UniqueViolationError:
            self._status_code = INTERNAL_SERVER_ERROR
    
class PostgreSqlUserSettingsSecretCode(PostgreSqlQueriesBase):
    def __init__(
            self,
            connection: PostgreSqlConnection,
            model_token: ModelToken,
            model_user_extend: ModelUserExtend
        ) -> None:
        super().__init__(connection)
        self.__model_user_extend: ModelUserExtend = model_user_extend
        self.__model_token: ModelToken = model_token
        self.__model_code = ModelCode()
        self.__secret_code: str
    
    @property
    def secret_code(self) -> str:
        return self.__secret_code

    async def execute(self):
        values = await self._connection.connection.fetch('''
        SELECT c_secret_code, c_backup_codes
        FROM c_codes
        JOIN u_users ON u_users.u_id = c_codes.c_u_id
        WHERE (
            SELECT TRUE
            FROM t_tokens
            WHERE t_token = $1
            AND active_token($1) = TRUE
        ) = TRUE
        AND u_users.u_secret_string = $2
        ''',
        self.__model_token.token,
        self.__model_user_extend.old_secret_string
        )

        if len(values) == 0:
            self._status_code = UNAUTHORIZED
            return

        for value in values:
            self.__secret_code = value['c_secret_code']

        self._response = self.__model_code
        self._status_code = OK
        return