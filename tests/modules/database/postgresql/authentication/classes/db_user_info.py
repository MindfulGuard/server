from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.user import PostgreSqlUser

class DbTestUserInfo:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_user_info = PostgreSqlUser(self.__connection)
        self.__model_token: ModelToken = ModelToken()

    async def get(self, token: str):
        try:
            self.__model_token.token = token
            db = self.__pgsql_user_info.get_tokens(self.__model_token)
            await self.__connection.open()
            await db.execute()
            return db.response
        finally:
            await self.__connection.close()