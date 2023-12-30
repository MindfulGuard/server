from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlUserSettingsDeleteAccount(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_user: ModelUser
    ) -> None:
        super().__init__(connection)
        self.__model_token: ModelToken = model_token
        self.__model_user: ModelUser =  model_user

    def secret_code(self):
        return PostgreSqlUserSettingsSecretCode(
            self._connection,
            self.__model_token,
            self.__model_user
        )
    
    async def execute(self, confirm: bool) -> None:
        value: int = await self._connection.connection.fetchval('''
        SELECT delete_user($1, $2, $3);
        ''',
        self.__model_token.token,
        self.__model_user.secret_string,
        confirm
        )
        print(value)
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

class PostgreSqlUserSettingsSecretCode(PostgreSqlQueriesBase):
    def __init__(
            self,
            connection: PostgreSqlConnection,
            model_token: ModelToken,
            model_user: ModelUser
        ) -> None:
        super().__init__(connection)
        self.__model_user: ModelUser = model_user
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
        self.__model_user.secret_string
        )

        if len(values) == 0:
            self._status_code = UNAUTHORIZED
            return

        for value in values:
            self.__secret_code = value['c_secret_code']

        self._response = self.__model_code
        self._status_code = OK
        return