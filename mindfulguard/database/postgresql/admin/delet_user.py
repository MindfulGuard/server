from http.client import INTERNAL_SERVER_ERROR, OK, UNAUTHORIZED
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlAdminDeletUser(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_user: ModelUser
    ) -> None:
        super().__init__(connection)
        self.__auth_is_auth_admin = PostgreSqlAuthentication(self._connection)
        self.__model_token: ModelToken = model_token
        self.__model_user: ModelUser = model_user

    async def execute(self) -> None:
        is_auth = self.__auth_is_auth_admin.is_auth_admin(
            self.__model_token
        )
        await is_auth.execute()

        if is_auth.status_code != OK:
            self._status_code = is_auth.status_code
            return
        
        value: int = await self._connection.connection.fetchval('''
        SELECT delete_user($1);
        ''',
        self.__model_user.id
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