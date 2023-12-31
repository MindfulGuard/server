from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.safe import ModelSafe
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.safe import PostgreSqlSafe


class DbTestDeleteSafe:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_safe: PostgreSqlSafe  = PostgreSqlSafe(self.__connection)
        self.__model_token: ModelToken = ModelToken()
        self.__model_safe: ModelSafe = ModelSafe()

    async def execute(
        self,
        token: str,
        safe_id: str
    ):
        try:
            self.__model_token.token = token
            self.__model_safe.id = safe_id
            db = self.__pgsql_safe.delete(self.__model_token, self.__model_safe)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()

    