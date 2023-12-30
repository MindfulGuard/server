from http.client import CONFLICT, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, SERVICE_UNAVAILABLE
import asyncpg
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.code import ModelCode
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlSignUp(PostgreSqlQueriesBase):
    """
    Requested values for ModelUser:
        ModelUser().login,
        ModelUser().secret_string,
        ModelUser().reg_ip,
        ModelUser().confirm

    Requested values for ModelCode:
        ModelCode().secret_code,
        ModelCode().backup_codes
    """
    def __init__(self, connection: PostgreSqlConnection, model_user: ModelUser, model_code: ModelCode) -> None:
        super().__init__(connection)
        self.__model_user: ModelUser = model_user
        self.__model_code: ModelCode = model_code
    
    async def execute(self) -> None:
        try:
            value: int = await self._connection.connection.fetchval('''
            SELECT sign_up($1, $2, $3, $4, $5,$6)
            ''',
            self.__model_user.login,
            self.__model_user.secret_string,
            self.__model_user.reg_ip,
            self.__model_user.confirm,
            self.__model_code.secret_code,
            self.__model_code.backup_codes
            )

            if value == 0 or value == 1 or value == 2:
                self._status_code = OK
                return
            elif value == -1:
                self._status_code = CONFLICT
                return
            elif value == -2 or value == -3 or value == -4:
                self._status_code = NOT_FOUND
                return
            elif value == -5:
                self._status_code = SERVICE_UNAVAILABLE
                return
            else:
                self._status_code = INTERNAL_SERVER_ERROR
                return

        except asyncpg.exceptions.DataError:
            self._status_code = INTERNAL_SERVER_ERROR
        except asyncpg.exceptions.UniqueViolationError:
            self._status_code = CONFLICT