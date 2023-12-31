from http.client import BAD_REQUEST, OK
from typing import Any
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.safe import PostgreSqlSafe


class DbTestGetSafe:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_safe: PostgreSqlSafe  = PostgreSqlSafe(self.__connection)
        self.__model_token: ModelToken = ModelToken()
        self.__response = Any

    @property
    def response(self):
        return self.__response

    async def execute(
        self,
        token: str
    ) -> int:
        try:
            self.__model_token.token = token
            db = self.__pgsql_safe.get(self.__model_token)
            await self.__connection.open()
            await db.execute()
            if db.status_code == OK:
                self.__response = db.response
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()