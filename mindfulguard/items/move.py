from http.client import BAD_REQUEST, OK
from mindfulguard.classes.items.base import ItemsBase
from mindfulguard.items.model_record_extend import ModelRecordExtend

class Move(ItemsBase):
    def __init__(self) -> None:
        super().__init__()
        self.__model_record_extend = ModelRecordExtend()

    async def execute(
        self,
        token: str,
        old_safe_id: str,
        new_safe_id: str,
        record_id: str
    ) -> None:
        try:
            self.__model_record_extend.old_safe_id = old_safe_id
            self.__model_record_extend.new_safe_id = new_safe_id
            if self.__model_record_extend.old_safe_id == self.__model_record_extend.new_safe_id:
                self._status_code = BAD_REQUEST
                return
            self._model_token.token = token
            self.__model_record_extend.id = record_id

            db = self._pgsql_items.move(self._model_token, self.__model_record_extend)
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            if db.status_code == OK:
                for i in self._redis.client().connection.scan_iter(
                    f'{self._model_token.token}:{self._redis.PATH_SAFE_ALL_ITEM}'
                ):
                    self._redis.client().connection.delete(i)
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()