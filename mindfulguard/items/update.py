import copy
from http.client import BAD_REQUEST, OK
import json
from typing import Any
from mindfulguard.classes.items.base import ItemsBase
from mindfulguard.classes.models.item_json import Item
from mindfulguard.classes.models.record import ModelRecord


class Update(ItemsBase):
    def __init__(self) -> None:
        super().__init__()

    class __ModelRecordExtend(ModelRecord):
        def __init__(self):
            super().__init__()

        @property
        def item(self) -> str:
            return json.dumps(self._item, ensure_ascii=False)

        @item.setter
        def item(self, value: dict[str, Any]) -> None:
            self._item = value

    async def execute(
        self,
        token: str,
        safe_id: str,
        record_id: str,
        model_item_json: Item
    ) -> None:
        try:
            model_record = self.__ModelRecordExtend()
            self._model_token.token = token
            model_record.safe_id = safe_id
            model_record.id = record_id

            model_item = Item(
                title=model_item_json.title,
                category=model_item_json.category,
                notes=model_item_json.notes,
                tags=model_item_json.tags,
                sections=model_item_json.sections
            )
            copied_item = copy.deepcopy(model_item)
            del copied_item.title, copied_item.category, copied_item.notes, copied_item.tags

            model_record.title = model_item.title
            model_record.item = copied_item.model_dump()
            model_record.notes = model_item.notes
            model_record.tags = model_item.tags
            model_record.category = model_item.category
            
            db = self._pgsql_items.update(self._model_token, model_record)
            db_user_info = self._pgsql_user.get_information(self._model_token)
            await self._connection.open()
            await db.execute()
            await db_user_info.execute()
            self._status_code = db.status_code
            if db.status_code == OK and db_user_info.status_code == OK:
                for i in self._redis.client().connection.scan_iter(
                    f'{db_user_info.response.login}:{self._redis.PATH_SAFE_ALL_ITEM}'
                ):
                    self._redis.client().connection.delete(i)
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()