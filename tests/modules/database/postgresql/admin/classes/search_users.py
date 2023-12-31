from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.models.user import ModelUser
from mindfulguard.database.postgresql.admin import PostgreSqlAdmin


class DbTestAdminSearchUsers:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_admin: PostgreSqlAdmin  = PostgreSqlAdmin(self.__connection)
        self.__model_token: ModelToken = ModelToken()
        self.__model_user = ModelUser()

    async def execute(self, token: str, user_id: str) -> int:
        try:
            self.__model_token.token = token
            self.__model_user.id = user_id
            
            db = self.__pgsql_admin.search_users(self.__model_token, self.__model_user)
            await self.__connection.open()
            await db.execute('id')
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()