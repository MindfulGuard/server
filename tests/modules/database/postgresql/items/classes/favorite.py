from http.client import BAD_REQUEST, OK
from typing import Any
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.items import PostgreSqlItems


class DbTestItemFavorite:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_items = PostgreSqlItems(self.__connection)
        self.__model_token = ModelToken()
        self.__model_record = ModelRecord()

    async def execute(
        self,
        token: str,
        item_id: str,
        safe_id: str
    ) -> int:
        try:
            self.__model_token.token = token
            self.__model_record.id = item_id
            self.__model_record.safe_id = safe_id
            db = self.__pgsql_items.favorite(self.__model_token, self.__model_record)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()