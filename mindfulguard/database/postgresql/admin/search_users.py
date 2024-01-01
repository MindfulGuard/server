from http.client import BAD_REQUEST, NOT_FOUND, OK
from mindfulguard.classes.database.postgresql.queries_base import PostgreSqlQueriesBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication
from mindfulguard.database.postgresql.connection import PostgreSqlConnection


class PostgreSqlAdminSearchUsers(PostgreSqlQueriesBase):
    def __init__(
        self,
        connection: PostgreSqlConnection,
        model_token: ModelToken,
        model_user: ModelUser
    ) -> None:
        super().__init__(connection)
        self.__auth_is_auth_admin = PostgreSqlAuthentication(self._connection)
        self.__model_token = model_token
        self.__model_user = model_user
        self.__model_user_response = ModelUser()
        
    @property
    def response(self) -> ModelUser:
        return self.__model_user_response

    async def execute(self, key: str) -> None:
        is_auth = self.__auth_is_auth_admin.is_auth_admin(
            self.__model_token
        )
        await is_auth.execute()

        if is_auth.status_code != OK:
            self._status_code = is_auth.status_code
            return
        
        query: str = "SELECT u_id, u_login, u_reg_ip, u_confirm, u_created_at FROM u_users"
        if key == "id":
            values = await self._connection.connection.fetch(
                f"{query} WHERE u_id = $1;",
                self.__model_user.id
            )

            if not values:
                self._status_code = NOT_FOUND
                return
            for i in values:
                self.__model_user_response.id = i['u_id']
                self.__model_user_response.login = i['u_login']
                self.__model_user_response.reg_ip = i['u_reg_ip']
                self.__model_user_response.confirm = i['u_confirm']
                self.__model_user_response.created_at = i['u_created_at']

            self._response = self.__model_user_response
            self._status_code = OK
            return
        elif key == "username":
            values = await self._connection.connection.fetch(
                f"{query} WHERE u_login = $1;",
                self.__model_user.login
            )
            if not values:
                self._status_code = NOT_FOUND
                return
            for i in values:
                self.__model_user_response.id = i['u_id']
                self.__model_user_response.login = i['u_login']
                self.__model_user_response.reg_ip = i['u_reg_ip']
                self.__model_user_response.confirm = i['u_confirm']
                self.__model_user_response.created_at = i['u_created_at']

            self._response = self.__model_user_response
            self._status_code = OK
            return
        else:
            self._status_code = BAD_REQUEST
            return