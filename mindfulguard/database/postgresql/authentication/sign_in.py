from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED
import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.totp_code import ModelTotpCode
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlSignIn(PostgreSqlQueriesBase):
    def __init__(
            self,
            connection: PostgreSqlConnection,
            model_user: ModelUser,
            model_token: ModelToken
        ) -> None:
        super().__init__(connection)
        self.__model_user: ModelUser = model_user
        self.__model_token: ModelToken = model_token
    
    def update_backup_codes(self, backup_codes: list[int]):
        return PostgreSqlSignInUpdateBackupCodes(
            self._connection,
            self.__model_user,
            backup_codes
        )

    def secret_code(self):
        """
        Return:
            ModelCode().secret_code,
            ModelCode().backup_codes
        """
        return PostgreSqlSignInSecretCode(self._connection, self.__model_user)

    async def execute(
            self,
            is_verified_code: bool
        ) -> None:
        try:
            value = await self._connection.connection.fetchval('''
            SELECT sign_in($1, $2, $3, $4, $5, $6, $7)
            ''',
            self.__model_user.login,
            self.__model_user.secret_string,
            self.__model_token.token,
            self.__model_token.device,
            self.__model_token.last_ip,
            self.__model_token.expiration,
            is_verified_code
            )
            if value:
                self._status_code = OK
                return
            else:
                self._status_code = NOT_FOUND
                return
        except asyncpg.exceptions.DataError:
            self._status_code = INTERNAL_SERVER_ERROR

class PostgreSqlSignInSecretCode(PostgreSqlQueriesBase):
    def __init__(
            self,
            connection: PostgreSqlConnection,
            model_user: ModelUser,
        ) -> None:
        super().__init__(connection)
        self.__model_user: ModelUser = model_user
        self.__model_code = ModelCode()
        self.__secret_code: str
        self.__backup_codes: list[int]
    
    @property
    def secret_code(self) -> str:
        return self.__secret_code

    @property
    def backup_codes(self) -> list[int]:
        return self.__backup_codes

    async def execute(self):
        values = await self._connection.connection.fetch('''
        SELECT c_secret_code, c_backup_codes
        FROM c_codes 
        JOIN u_users ON u_users.u_id = c_codes.c_u_id 
        WHERE u_users.u_login = $1
        AND u_users.u_secret_string = $2
        ''',
        self.__model_user.login,
        self.__model_user.secret_string
        )

        if len(values) == 0:
            self._status_code = UNAUTHORIZED
            return

        for value in values:
            self.__secret_code = value['c_secret_code']
            self.__backup_codes = value['c_backup_codes']

        self._response = self.__model_code
        self._status_code = OK
        return
    
class PostgreSqlSignInUpdateBackupCodes(PostgreSqlQueriesBase):
    def __init__(
            self,
            connection: PostgreSqlConnection,
            model_user: ModelUser,
            backup_codes: list[int]
        ) -> None:
        super().__init__(connection)
        self.__model_user: ModelUser = model_user
        self.__backup_codes: list[int] = backup_codes

    async def execute(self) -> None:
        value = await self._connection.connection.fetch(
            '''
            UPDATE c_codes SET c_backup_codes = $3
            WHERE c_u_id =(
                SELECT u_id FROM u_users
                WHERE u_login = $1 AND u_users.u_secret_string = $2
                )
            RETURNING c_id;
            ''',
            self.__model_user.login,
            self.__model_user.secret_string,
            self.__backup_codes
        )
        if value:
            self._status_code = OK
            return
        else:
            self._status_code = NOT_FOUND
            return