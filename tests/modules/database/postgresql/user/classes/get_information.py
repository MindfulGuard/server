from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.user import PostgreSqlUser


class DbTestUserInformationGet:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_user: PostgreSqlUser  = PostgreSqlUser(self.__connection)
        self.__model_token: ModelToken = ModelToken()

    async def execute(self, token: str) -> int:
        try:
            self.__model_token.token = token
            db = self.__pgsql_user.get_information(self.__model_token)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()