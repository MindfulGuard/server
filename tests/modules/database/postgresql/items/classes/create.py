from http.client import BAD_REQUEST
import json
from typing import Any
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.record import ModelRecord
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.items import PostgreSqlItems


class DbTestItemCreate:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_items = PostgreSqlItems(self.__connection)
        self.__model_token = ModelToken()
        self.__model_record = ModelRecord()

    async def execute(
        self,
        token: str,
        safe_id: str,
        title: str,
        item: dict[str, Any],
        notes: str,
        tags: list[str],
        category: str
    ) -> int:
        try:
            self.__model_token.token = token
            self.__model_record.safe_id = safe_id
            self.__model_record.title = title
            self.__model_record.item = json.dumps(item) # type: ignore
            self.__model_record.notes = notes
            self.__model_record.tags = tags
            self.__model_record.category = category

            db = self.__pgsql_items.create(self.__model_token, self.__model_record)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()