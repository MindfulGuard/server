import copy
from http.client import BAD_REQUEST
import json
from typing import Any
from mindfulguard.classes.items.base import ItemsBase
from mindfulguard.classes.models.item_json import Item
from mindfulguard.classes.models.record import ModelRecord


class Create(ItemsBase):
    def __init__(self) -> None:
        super().__init__()
    
    class __ModelRecordExtend(ModelRecord):
        def __init__(self):
            super().__init__()
            self.__safe_id: str
            self.__title: str
            self.__item: dict[str, Any]
            self.__notes: str
            self.__tags: list[str]
            self.__category: str

        @property
        def safe_id(self) -> str:
            return self.__safe_id
        
        @safe_id.setter
        def safe_id(self, value: str) -> None:
            if not self._validation.is_uuid(value):
                raise ValueError('The value is not a uuid')
            self.__safe_id = value

        @property
        def title(self) -> str:
            return self.__title
        
        @title.setter
        def title(self, value: str) -> None:
            self.__title = value

        @property
        def item(self) -> str:
            return json.dumps(self.__item, ensure_ascii=False)

        @item.setter
        def item(self, value: dict[str, Any]) -> None:
            self.__item = value

        @property
        def notes(self) -> str:
            return self.__notes
        
        @notes.setter
        def notes(self, value: str) -> None:
            self.__notes = value

        @property
        def tags(self) -> list[str]:
            return self.__tags
        
        @tags.setter
        def tags(self, value: list[str]) -> None:
            self.__tags = value

        @property
        def category(self) -> str:
            return self.__category
        
        @category.setter
        def category(self, value: str) -> None:
            self.__category = value

    async def execute(
        self,
        token: str,
        safe_id: str,
        model_item_json: Item
    ) -> None:
        try:
            model_record = self.__ModelRecordExtend()
            self._model_token.token = token
            model_record.safe_id = safe_id
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
            
            db = self._pgsql_items.create(self._model_token, model_record)
            await self._connection.open()
            await db.execute()
            self._status_code = db.status_code
            return
        except ValueError:
            self._status_code = BAD_REQUEST
        finally:
            await self._connection.close()