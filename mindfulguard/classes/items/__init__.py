from typing import Any
from fastapi import Response
from mindfulguard.classes.models.item_json import Item
from mindfulguard.classes.responses import Responses
from mindfulguard.items.create import Create
from mindfulguard.items.delete import Delete
from mindfulguard.items.favorite import Favorite
from mindfulguard.items.move import Move
from mindfulguard.items.update import Update

class Items:
    def __init__(self, response: Response) -> None:
        self.__responses = Responses()
        self.__response: Response = response

    async def create(self, token: str, safe_id: str, item: Item) -> dict[str, Any]:
        obj = Create()
        await obj.execute(token, safe_id, item)
        self.__response.status_code = obj.status_code
        response = self.__responses.default(
            ok = self.__responses.custom().get("item_was_successfully_created"),
            internal_server_error = self.__responses.custom().get("failed_to_create_item")
        ).get(obj.status_code)
        return response
    
    async def update(
        self,
        token: str,
        safe_id: str,
        record_id: str,
        item: Item
    ) -> dict[str, Any]:
        obj = Update()
        await obj.execute(
            token,
            safe_id,
            record_id,
            item
        )
        self.__response.status_code = obj.status_code
        response = self.__responses.default(
            ok = self.__responses.custom().get("item_has_been_successfully_updated"),
            internal_server_error = self.__responses.custom().get("failed_to_update_the_item")
        ).get(obj.status_code)
        return response
    
    async def delete(
        self,
        token: str,
        safe_id: str,
        record_id: str
    ) -> dict[str, Any]:
        obj = Delete()
        await obj.execute(
            token,
            safe_id,
            record_id
        )
        self.__response.status_code = obj.status_code
        response = self.__responses.default(
            ok = self.__responses.custom().get("item_was_successfully_deleted"),
            internal_server_error = self.__responses.custom().get("failed_to_delete_item")
        ).get(obj.status_code)
        return response
    
    async def favorite(
        self,
        token: str,
        safe_id: str,
        record_id: str
    ) -> dict[str, Any]:
        obj = Favorite()
        await obj.execute(token, safe_id, record_id)
        self.__response.status_code = obj.status_code

        response = self.__responses.default(
            ok = self.__responses.custom().get("item_was_successfully_added_to_favorites"),
            internal_server_error = self.__responses.custom().get("failed_to_update_favorite")
        ).get(obj.status_code)
        return response
    
    async def move(
        self,
        token: str,
        old_safe_id: str,
        new_safe_id: str,
        record_id: str
    ) -> dict[str, Any]:
        obj = Move()
        await obj.execute(
            token,
            old_safe_id,
            new_safe_id,
            record_id
        )
        self.__response.status_code = obj.status_code

        response = self.__responses.default(
            ok = self.__responses.custom().get("item_was_successfully_moved_to_safe"),
            internal_server_error = self.__responses.custom().get("failed_to_move_item_to_safe")
        ).get(obj.status_code)
        return response