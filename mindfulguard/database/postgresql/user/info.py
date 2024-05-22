from http.client import OK, UNAUTHORIZED
import time
from typing import Any

from loguru import logger
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.authentication.is_auth import PostgreSqlIsAuth
from mindfulguard.database.postgresql.connection import PostgreSqlConnection
from mindfulguard.exceptions.incorrect_parameters import ExceptionIncorrectParameters


class PostgreSqlUserInformation(PostgreSqlQueriesBase):
    def __init__(self, connection: PostgreSqlConnection, model_token: ModelToken) -> None:
        super().__init__(connection)
        self.__pgsql_is_auth = PostgreSqlIsAuth(self._connection, model_token)
        self.__model_token: ModelToken = model_token
        self.__model_user = ModelUser()

    @property
    def response(self) -> ModelUser:
        return self._response

    async def execute(self) -> None:
        start_time = time.time()
        logger.debug("Retrieving user information...")
        try:
            await self.__pgsql_is_auth.execute()
            if self.__pgsql_is_auth.status_code == UNAUTHORIZED:
                self._status_code = self.__pgsql_is_auth.status_code
                return

            values = await self._connection.connection.fetch(f'''
            SELECT u_login, u_reg_ip, u_created_at FROM u_users
            WHERE u_id = (
                SELECT t_u_id FROM t_tokens
                WHERE t_token = $1
                );
            ''',
            self.__model_token.token
            )
            
            for i in values:
                self.__model_user.login = i['u_login']
                self.__model_user.created_at = i['u_created_at']
                self.__model_user.reg_ip = i['u_reg_ip']

            self._response = self.__model_user
            self._status_code = OK
            return
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.trace("Retrieving user information execution time: {} seconds", execution_time)