from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.admin import PostgreSqlAdmin


class DbTestAdminGetByPage:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_admin: PostgreSqlAdmin  = PostgreSqlAdmin(self.__connection)
        self.__model_token: ModelToken = ModelToken()

    async def execute(self, token: str) -> int:
        try:
            self.__model_token.token = token
            db = self.__pgsql_admin.get_users(self.__model_token)
            await self.__connection.open()
            await db.execute(10, 2)
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()