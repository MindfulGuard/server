from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED

import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlUserSettingsUpdateOneTimeCode:
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_user: ModelUser,
        model_code: ModelCode
    ) -> None:
        self.__connection = connection
        self.__model_user: ModelUser = model_user
        self.__model_token: ModelToken = model_token
        self.__model_code: ModelCode = model_code

    def totp(self):
        return PostgreSqlUserSettingsUpdateOneTimeCodeTotp(
            self.__connection,
            self.__model_user,
            self.__model_token,
            self.__model_code
        )

    def backup(self):
        return PostgreSqlUserSettingsUpdateOneTimeCodeBackup(
            self.__connection,
            self.__model_user,
            self.__model_token,
            self.__model_code
        )

class PostgreSqlUserSettingsUpdateOneTimeCodeTotp(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_user: ModelUser,
        model_token: ModelToken,
        model_code: ModelCode
    ) -> None:
        super().__init__(connection)
        self.__model_user: ModelUser = model_user
        self.__model_token: ModelToken = model_token
        self.__model_code: ModelCode = model_code

    async def execute(self) -> None:
        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT update_c_codes_code($1, $2, $3);
            ''',
            self.__model_token.token,
            self.__model_user.secret_string,
            self.__model_code.secret_code
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

class PostgreSqlUserSettingsUpdateOneTimeCodeBackup(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_user: ModelUser,
        model_token: ModelToken,
        model_code: ModelCode
    ) -> None:
        super().__init__(connection)
        self.__model_user: ModelUser = model_user
        self.__model_token: ModelToken = model_token
        self.__model_code: ModelCode = model_code

    async def execute(self) -> None:
        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT update_c_codes_code($1, $2, $3::INTEGER[]);
            ''',
            self.__model_token.token,
            self.__model_user.secret_string,
            self.__model_code.backup_codes
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