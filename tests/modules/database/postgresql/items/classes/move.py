from http.client import BAD_REQUEST
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.database.postgresql.items import PostgreSqlItems
from mindfulguard.items.model_record_extend import ModelRecordExtend


class DbTestItemMove:
    def __init__(self) -> None:
        self.__connection = DataBase().postgresql().connection()
        self.__pgsql_items = PostgreSqlItems(self.__connection)
        self.__model_token = ModelToken()
        self.__model_record_extend = ModelRecordExtend()

    async def execute(
        self,
        token: str,
        item_id: str,
        old_safe_id: str,
        new_safe_id: str
    ) -> int:
        try:
            self.__model_token.token = token
            self.__model_record_extend.id = item_id
            self.__model_record_extend.old_safe_id = old_safe_id
            self.__model_record_extend.new_safe_id = new_safe_id

            db = self.__pgsql_items.move(self.__model_token, self.__model_record_extend)
            await self.__connection.open()
            await db.execute()
            return db.status_code
        except ValueError:
            return BAD_REQUEST
        finally:
            await self.__connection.close()